import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class AgentLedgerPolicyTests(unittest.TestCase):
    def event(self):
        return {
            "schema_version": "1.0", "event_id": "policy-start-1",
            "timestamp_utc": "2026-07-19T00:00:00Z", "agent_run_id": "policy-run",
            "parent_task": "root", "agent_name": "terra_worker",
            "requested_model": "gpt-5.6-terra", "requested_reasoning": "low",
            "task_type": "test", "roadmap_step": None, "event_type": "started",
            "status": "started", "scope_summary": "Temporary policy validation.",
            "constraints": [], "commands": ["temporary test"], "files_changed": [],
            "git_commit_before": None, "git_commit_after": None,
            "ml_ledger_event_ids": [], "outcome_summary": None,
            "supervisor_decision": None, "duration_seconds": None, "notes": "fixture",
        }

    def rejects_without_mutation(self, mutate):
        with tempfile.TemporaryDirectory() as directory:
            ledger = Path(directory) / "ledger.jsonl"
            event = self.event(); mutate(event)
            before = json.dumps(event, separators=(",", ":")).encode() + b"\n"
            ledger.write_bytes(before)
            result = subprocess.run(
                [sys.executable, str(ROOT / "tools" / "agent_ledger.py"), "--ledger", str(ledger), "validate"],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 2)
            self.assertEqual(ledger.read_bytes(), before)

    def test_rejects_status_timestamp_and_secret_without_mutation(self):
        for mutate in (
            lambda event: event.update(status="completed"),
            lambda event: event.update(timestamp_utc="not-a-time"),
            lambda event: event.update(notes="api" + "_key=do-not-record"),
        ):
            with self.subTest(mutate=mutate):
                self.rejects_without_mutation(mutate)

    def test_correction_is_helper_appended(self):
        with tempfile.TemporaryDirectory() as directory:
            ledger = Path(directory) / "ledger.jsonl"
            ledger.write_text(json.dumps(self.event()) + "\n", encoding="utf-8")
            command = [
                sys.executable, str(ROOT / "tools" / "agent_ledger.py"),
                "--ledger", str(ledger), "correction", "--event-id", "policy-start-1",
                "--outcome-summary", "Corrected fixture.", "--notes", "fixture correction",
            ]
            self.assertEqual(subprocess.run(command).returncode, 0)
            events = [json.loads(line) for line in ledger.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(events[-1]["event_type"], "correction")
            self.assertEqual(events[-1]["status"], "corrected")


if __name__ == "__main__":
    unittest.main()
