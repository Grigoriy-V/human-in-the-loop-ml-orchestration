import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ScaffoldTests(unittest.TestCase):
    def command(self, *arguments):
        return subprocess.run(
            [sys.executable, *arguments],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=30,
        )

    def test_local_validators(self):
        for command in (
            ("tools/validate_core_pin.py",),
            ("tools/agent_ledger.py", "validate"),
            ("tools/validate_orchestration.py",),
        ):
            with self.subTest(command=command):
                result = self.command(*command)
                self.assertEqual(
                    result.returncode,
                    0,
                    msg=f"stdout={result.stdout}\nstderr={result.stderr}",
                )

    def test_adapter_inventory_boundary(self):
        lock = json.loads(
            (ROOT / "orchestration.lock.json").read_text(encoding="utf-8")
        )
        classical = {
            "ML_PROJECT_ROADMAP.md",
            "docs/classical_ml_adapter.md",
            "tools/experiment_ledger.py",
            "reports/experiment_ledger.schema.json",
            "reports/experiment_ledger.jsonl",
            "tests/test_classical_contract.py",
        }
        if lock["adapter_type"] == "generic":
            self.assertTrue(all(not (ROOT / path).exists() for path in classical))
            self.assertTrue((ROOT / "PROJECT_ROADMAP.md").is_file())
            self.assertFalse((ROOT / "ML_PROJECT_ROADMAP.md").exists())
        else:
            self.assertEqual(lock["adapter_type"], "classical_ml")
            self.assertTrue(all((ROOT / path).is_file() for path in classical))
            self.assertFalse((ROOT / "PROJECT_ROADMAP.md").exists())
            self.assertTrue((ROOT / "ML_PROJECT_ROADMAP.md").is_file())

    def test_mutable_evidence_is_not_managed(self):
        lock = json.loads(
            (ROOT / "orchestration.lock.json").read_text(encoding="utf-8")
        )
        managed = {entry["target_path"] for entry in lock["managed_files"]}
        self.assertTrue(
            {
                "PROJECT_LOG.md",
                "PROJECT_ROADMAP.md",
                "ML_PROJECT_ROADMAP.md",
                "reports/agent_execution_ledger.jsonl",
                "reports/experiment_ledger.jsonl",
            }.isdisjoint(managed)
        )


if __name__ == "__main__":
    unittest.main()
