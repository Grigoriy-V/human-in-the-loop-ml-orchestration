import copy
import hashlib
import json
import sys
import tempfile
import unittest
import uuid
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import experiment_ledger as ledger

H1, H2, H3 = "1" * 64, "2" * 64, "3" * 64


def runtime():
    return {
        "python_version": "3.13.5",
        "platform": "contract-test",
        "executor": "unittest",
        "packages": {"scikit-learn": "1.7.0"},
    }


def dataset():
    return {
        "name": "conversion-events-v1",
        "source": "governed-internal-snapshot",
        "license": "internal-approved-use",
        "fingerprint_sha256": H1,
        "target": {
            "column": "converted",
            "task_type": "binary_classification",
            "positive_class": 1,
        },
    }


def pipeline():
    return {
        "library": "sklearn",
        "class": "sklearn.pipeline.Pipeline",
        "steps": [
            {
                "name": "preprocess",
                "class": "sklearn.compose.ColumnTransformer",
                "params": {"remainder": "drop"},
            },
            {
                "name": "model",
                "class": "sklearn.linear_model.LogisticRegression",
                "params": {"C": 1.0, "random_state": 17},
            },
        ],
    }


def baseline_cv():
    return {
        "baseline_model": {
            "class": "sklearn.linear_model.LogisticRegression",
            "params": {"C": 1.0, "random_state": 17},
        },
        "cv": {
            "strategy": "StratifiedKFold",
            "folds": 5,
            "shuffle": True,
            "random_state": 17,
        },
        "metrics": {"roc_auc_mean": 0.71, "average_precision_mean": 0.36},
        "primary_metric": "roc_auc_mean",
    }


def caller(operation="dataset_audit", status="completed", experiment="exp-001"):
    event = {
        "schema_version": "2.0",
        "experiment_id": experiment,
        "operation": operation,
        "status": status,
        "commands": [],
        "runtime": None,
        "dataset": None,
        "leakage_audit": None,
        "split": None,
        "features": None,
        "pipeline": None,
        "baseline_cv": None,
        "calibration": None,
        "threshold": None,
        "artifacts": [],
        "decision": {"action": "pending", "rationale": "Awaiting approved action."},
    }
    if status == "completed":
        event["commands"] = [f"python run_{operation}.py --config approved.json"]
        event["runtime"] = runtime()
        event["dataset"] = dataset()
        event["decision"] = {
            "action": "freeze" if operation == "closeout" else "continue",
            "rationale": f"{operation} satisfies the approved acceptance contract.",
        }
        if operation == "dataset_audit":
            event["leakage_audit"] = {
                "checked": True,
                "methods": ["target-origin review", "post-outcome review"],
                "findings": [],
                "prohibited_features": ["converted", "conversion_timestamp"],
            }
            event["split"] = {
                "strategy": "random",
                "random_state": 17,
                "stratified": True,
                "stratify_by": "converted",
                "train_fingerprint_sha256": H2,
                "test_fingerprint_sha256": H3,
            }
            event["features"] = {
                "included": ["channel", "sessions"],
                "categorical": ["channel"],
                "numeric": ["sessions"],
                "excluded": ["converted", "conversion_timestamp"],
            }
        elif operation == "baseline":
            event["pipeline"], event["baseline_cv"] = pipeline(), baseline_cv()
        elif operation == "evaluation":
            event["pipeline"], event["baseline_cv"] = pipeline(), baseline_cv()
            event["calibration"] = {
                "method": "sigmoid",
                "cv_folds": 5,
                "metrics_before": {"brier": 0.20},
                "metrics_after": {"brier": 0.18},
            }
            event["threshold"] = {
                "value": 0.42,
                "objective": "maximize expected intervention value",
                "selection_split": "train_cv_oof",
                "metric_name": "f1",
                "metric_value": 0.48,
            }
    elif status == "failed":
        event["commands"] = [f"python run_{operation}.py --config approved.json"]
        event["runtime"] = runtime()
        event["decision"] = {
            "action": "change",
            "rationale": "The command failed before valid results were produced.",
        }
    elif status == "skipped":
        event["decision"] = {
            "action": "stop",
            "rationale": "The approved stage was skipped without results.",
        }
    return event


def stored(event, sequence):
    event = copy.deepcopy(event)
    event["event_id"] = str(uuid.UUID(int=sequence, version=4))
    event["timestamp_utc"] = f"2026-01-01T00:00:{sequence:02d}.000000Z"
    return event


class ClassicalLedgerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "reports").mkdir()
        self.path = self.root / "reports" / "experiment.jsonl"

    def tearDown(self):
        self.temp.cleanup()

    def test_all_operation_status_contract_families(self):
        for operation in ledger.OPERATIONS:
            for status in ledger.STATUSES:
                with self.subTest(operation=operation, status=status):
                    ledger.validate_event(
                        stored(caller(operation, status), 1), root=self.root
                    )

    def test_helper_generates_uuid4_utc_and_cleans_lock(self):
        before = datetime.now(timezone.utc)
        result = ledger.append_event(caller(), self.path, root=self.root)
        after = datetime.now(timezone.utc)
        timestamp = datetime.fromisoformat(
            result["timestamp_utc"][:-1] + "+00:00"
        )
        self.assertEqual(uuid.UUID(result["event_id"]).version, 4)
        self.assertLessEqual(before, timestamp)
        self.assertLessEqual(timestamp, after)
        self.assertFalse(Path(str(self.path) + ".lock").exists())

    def test_caller_generated_fields_and_invalid_candidate_preserve_bytes(self):
        first = ledger.append_event(caller(), self.path, root=self.root)
        before = self.path.read_bytes()
        bad = caller("closeout")
        bad["event_id"], bad["timestamp_utc"] = (
            first["event_id"],
            first["timestamp_utc"],
        )
        with self.assertRaises(ledger.LedgerError):
            ledger.append_event(bad, self.path, root=self.root)
        self.assertEqual(before, self.path.read_bytes())
        self.assertFalse(Path(str(self.path) + ".lock").exists())

    def test_lifecycle_identity_duplicate_and_order(self):
        audit = stored(caller(), 1)
        baseline = stored(caller("baseline"), 2)
        evaluation = stored(caller("evaluation"), 3)
        ledger.validate_sequence([audit, baseline, evaluation])

        duplicate = copy.deepcopy(baseline)
        duplicate["event_id"] = audit["event_id"]
        with self.assertRaises(ledger.LedgerError):
            ledger.validate_sequence([audit, duplicate])

        drift = copy.deepcopy(baseline)
        drift["dataset"]["fingerprint_sha256"] = "a" * 64
        with self.assertRaises(ledger.LedgerError):
            ledger.validate_sequence([audit, drift])

        regressed = stored(caller(), 4)
        with self.assertRaises(ledger.LedgerError):
            ledger.validate_sequence([audit, baseline, regressed])

        with self.assertRaises(ledger.LedgerError):
            ledger.validate_sequence([stored(caller("baseline"), 1)])

    def test_invalid_timestamp_rejected_by_full_ledger_validation(self):
        event = stored(caller(), 1)
        event["timestamp_utc"] = "2026-02-30T00:00:00Z"
        self.path.write_text(json.dumps(event) + "\n", encoding="utf-8")
        before = self.path.read_bytes()
        with self.assertRaises(ledger.LedgerError):
            ledger.validate_ledger(self.path, root=self.root)
        self.assertEqual(before, self.path.read_bytes())

    def test_strict_dataset_leakage_split_pipeline_cv_and_evaluation(self):
        mutations = []
        bad = stored(caller(), 1)
        bad["dataset"]["license"] = "unknown"
        mutations.append(bad)
        bad = stored(caller(), 1)
        bad["dataset"]["target"]["task_type"] = "regression"
        mutations.append(bad)
        bad = stored(caller(), 1)
        bad["features"]["included"].append("converted")
        bad["features"]["numeric"].append("converted")
        mutations.append(bad)
        bad = stored(caller(), 1)
        bad["split"]["random_state"] = None
        mutations.append(bad)
        bad = stored(caller("baseline"), 1)
        bad["pipeline"]["steps"][0]["params"] = {}
        mutations.append(bad)
        bad = stored(caller("baseline"), 1)
        bad["baseline_cv"]["cv"]["folds"] = 1
        mutations.append(bad)
        bad = stored(caller("evaluation"), 1)
        bad["calibration"] = {}
        mutations.append(bad)
        bad = stored(caller("evaluation"), 1)
        bad["threshold"]["value"] = 1.5
        mutations.append(bad)
        for event in mutations:
            with self.subTest(index=mutations.index(event)):
                with self.assertRaises(ledger.LedgerError):
                    ledger.validate_event(event, root=self.root)

    def artifact_event(self, path, digest):
        event = stored(caller(), 1)
        event["artifacts"] = [{"path": path, "sha256": digest}]
        return event

    def test_artifact_path_presence_hash_and_nonhex(self):
        artifact = self.root / "reports" / "audit.txt"
        artifact.write_bytes(b"audited")
        digest = hashlib.sha256(b"audited").hexdigest()
        ledger.validate_event(
            self.artifact_event("reports/audit.txt", digest), root=self.root
        )
        traversal = (PurePosixPath("..") / "outside.txt").as_posix()
        cases = [
            self.artifact_event(traversal, digest),
            self.artifact_event("reports/missing.txt", digest),
            self.artifact_event("reports/audit.txt", "z" * 64),
            self.artifact_event("reports/audit.txt", "0" * 64),
        ]
        for event in cases:
            with self.subTest(index=cases.index(event)):
                with self.assertRaises(ledger.LedgerError):
                    ledger.validate_event(event, root=self.root)

    def _symlink(self, link, target, directory=False):
        try:
            link.symlink_to(target, target_is_directory=directory)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"symlink unavailable: {exc}")

    def test_artifact_symlink_file_and_parent_rejected(self):
        real = self.root / "reports" / "real.txt"
        real.write_bytes(b"real")
        digest = hashlib.sha256(b"real").hexdigest()
        link = self.root / "reports" / "link.txt"
        self._symlink(link, real)
        with self.assertRaises(ledger.LedgerError):
            ledger.validate_event(
                self.artifact_event("reports/link.txt", digest), root=self.root
            )
        link.unlink()
        directory = self.root / "real-directory"
        directory.mkdir()
        (directory / "value.txt").write_bytes(b"real")
        linked = self.root / "linked-directory"
        self._symlink(linked, directory, directory=True)
        with self.assertRaises(ledger.LedgerError):
            ledger.validate_event(
                self.artifact_event("linked-directory/value.txt", digest),
                root=self.root,
            )

    def test_stale_or_concurrent_lock_fails_closed(self):
        self.path.write_bytes(b"")
        lock = Path(str(self.path) + ".lock")
        lock.write_text('{"pid":999999}', encoding="utf-8")
        before = self.path.read_bytes()
        with self.assertRaises(ledger.LedgerError):
            ledger.append_event(caller(), self.path, root=self.root)
        self.assertEqual(before, self.path.read_bytes())
        self.assertTrue(lock.exists())

    def test_noncompleted_events_cannot_fabricate_results(self):
        for status in ("failed", "skipped", "pending"):
            event = stored(caller(status=status), 1)
            event["dataset"] = dataset()
            with self.subTest(status=status):
                with self.assertRaises(ledger.LedgerError):
                    ledger.validate_event(event, root=self.root)


if __name__ == "__main__":
    unittest.main()
