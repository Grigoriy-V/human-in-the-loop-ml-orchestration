import copy
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CoreV02Tests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temporary.name)
        self.snapshot = self.workspace / "core"
        shutil.copytree(
            ROOT,
            self.snapshot,
            ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc", "*.lock"),
        )
        self.execute(["git", "init", "-q", self.snapshot])
        self.execute(["git", "-C", self.snapshot, "config", "user.email", "test@example.invalid"])
        self.execute(["git", "-C", self.snapshot, "config", "user.name", "Core Contract Test"])
        self.execute(["git", "-C", self.snapshot, "config", "core.autocrlf", "false"])
        self.execute(["git", "-C", self.snapshot, "add", "."])
        self.execute(["git", "-C", self.snapshot, "commit", "-q", "-m", "fixture"])
        self.commit = self.execute(
            ["git", "-C", self.snapshot, "rev-parse", "HEAD"]
        ).stdout.strip()

    def tearDown(self):
        self.temporary.cleanup()

    def execute(self, command, *, cwd=None, expected=0):
        result = subprocess.run(
            command,
            cwd=cwd or self.workspace,
            capture_output=True,
            text=True,
            timeout=120,
        )
        self.assertEqual(
            result.returncode,
            expected,
            msg=(
                f"command={command}\n"
                f"stdout={result.stdout}\n"
                f"stderr={result.stderr}"
            ),
        )
        return result

    def core(self, *arguments, expected=0):
        return self.execute(
            [sys.executable, *arguments],
            cwd=self.snapshot,
            expected=expected,
        )

    def bootstrap(self, adapter_type, name=None):
        target = self.workspace / (name or adapter_type)
        self.core(
            "tools/bootstrap_project.py",
            "--target",
            str(target),
            "--adapter-type",
            adapter_type,
            "--adapter-name",
            name or adapter_type,
        )
        return target

    def target(self, root, *arguments, expected=0):
        return self.execute(
            [sys.executable, *arguments], cwd=root, expected=expected
        )

    def test_core_validator_manifest_and_template_registry(self):
        self.core("tools/validate_orchestration.py")
        manifest = json.loads(
            (self.snapshot / "orchestration_manifest.json").read_text()
        )
        self.assertEqual(manifest["core_version"], "0.2.0")
        self.assertEqual(
            manifest["core_repository"], "human-in-the-loop-ml-orchestration"
        )
        self.assertNotIn("PROJECT_LOG.md", manifest["owned_files"])
        self.assertNotIn(
            "reports/agent_execution_ledger.jsonl", manifest["owned_files"]
        )
        self.assertIn("templates/adapters.json", manifest["owned_files"])
        self.assertIn(
            "templates/adapters/classical_ml/tools/experiment_ledger.py",
            manifest["owned_files"],
        )

    def test_dirty_source_unknown_adapter_and_dry_run_fail_closed(self):
        unknown = self.workspace / "unknown"
        self.core(
            "tools/bootstrap_project.py",
            "--target",
            str(unknown),
            "--adapter-type",
            "not_declared",
            "--adapter-name",
            "Unknown",
            expected=2,
        )
        self.assertFalse(unknown.exists())

        dry_target = self.workspace / "dry"
        self.core(
            "tools/bootstrap_project.py",
            "--dry-run",
            "--target",
            str(dry_target),
            "--adapter-type",
            "generic",
            "--adapter-name",
            "Dry",
        )
        self.assertFalse(dry_target.exists())

        with (self.snapshot / "README.md").open("a", encoding="utf-8") as handle:
            handle.write("\ndirty source fixture\n")
        dirty_target = self.workspace / "dirty-output"
        self.core(
            "tools/bootstrap_project.py",
            "--target",
            str(dirty_target),
            "--adapter-type",
            "generic",
            "--adapter-name",
            "Dirty",
            expected=2,
        )
        self.assertFalse(dirty_target.exists())

    def test_generic_and_classical_isolated_bootstrap_inventories_and_suites(self):
        generic = self.bootstrap("generic")
        classical = self.bootstrap("classical_ml")
        for target, expected_count in ((generic, 24), (classical, 28)):
            lock = json.loads(
                (target / "orchestration.lock.json").read_text(encoding="utf-8")
            )
            self.assertEqual(lock["core_commit"], self.commit)
            self.assertEqual(lock["core_version"], "0.2.0")
            self.assertEqual(len(lock["managed_files"]), expected_count)
            self.target(target, "tools/validate_core_pin.py")
            self.target(
                target,
                "tools/validate_core_pin.py",
                "--core-root",
                str(self.snapshot),
            )
            self.target(target, "tools/validate_orchestration.py")
            self.target(target, "-m", "unittest", "discover", "-s", "tests", "-v")

        classical_paths = {
            "ML_PROJECT_ROADMAP.md",
            "docs/classical_ml_adapter.md",
            "tools/experiment_ledger.py",
            "reports/experiment_ledger.schema.json",
            "reports/experiment_ledger.jsonl",
            "tests/test_classical_contract.py",
        }
        self.assertTrue(all(not (generic / path).exists() for path in classical_paths))
        self.assertTrue(all((classical / path).is_file() for path in classical_paths))
        self.assertFalse((generic / "reports/experiment_ledger.schema.json").exists())
        self.assertNotIn("experiment_ledger", (generic / "AGENTS.md").read_text())
        self.assertIn("semi-automatic", (classical / "AGENTS.md").read_text())
        self.assertIn('model_reasoning_effort = "none"', (classical / ".codex/agents/luna_clerk.toml").read_text())
        self.assertIn('model_reasoning_effort = "low"', (classical / ".codex/agents/terra_worker.toml").read_text())
        self.assertIn('model_reasoning_effort = "high"', (classical / ".codex/agents/sol_specialist.toml").read_text())

    def test_full_target_lifecycle_uses_powershell_metadata_file(self):
        target = self.bootstrap("generic")
        powershell = shutil.which("powershell")
        self.assertIsNotNone(powershell, "PowerShell is required by this acceptance test")
        metadata = {
            "agent_run_id": "powershell-lifecycle",
            "parent_task": "/root",
            "agent_name": "terra_worker",
            "requested_model": "gpt-5.6-terra",
            "requested_reasoning": "low",
            "task_type": "validation",
            "roadmap_step": None,
            "scope_summary": "Disposable adapter lifecycle.",
            "constraints": ["No external mutation"],
            "commands": ["PowerShell metadata-file start"],
            "files_changed": [],
            "git_commit_before": None,
            "git_commit_after": None,
            "ml_ledger_event_ids": [],
            "notes": "Isolated acceptance fixture.",
        }
        (target / "task-start.json").write_text(
            json.dumps(metadata), encoding="utf-8"
        )
        self.execute(
            [
                powershell,
                "-NoProfile",
                "-Command",
                "python tools/agent_ledger.py start --metadata-file task-start.json",
            ],
            cwd=target,
        )
        self.target(
            target,
            "tools/agent_ledger.py",
            "terminal",
            "--run-id",
            "powershell-lifecycle",
            "--status",
            "completed",
            "--outcome-summary",
            "Lifecycle fixture completed.",
            "--files-changed-json",
            "[]",
            "--commands-json",
            '["isolated validation"]',
        )
        self.target(
            target,
            "tools/agent_ledger.py",
            "review",
            "--run-id",
            "powershell-lifecycle",
            "--decision",
            "accept",
            "--outcome-summary",
            "Lifecycle fixture accepted.",
            "--reviewer-agent-name",
            "root_supervisor",
            "--reviewer-model",
            "root-session-model",
            "--reviewer-reasoning",
            "not_applicable",
            "--parent-task",
            "/root",
        )
        result = self.target(target, "tools/agent_ledger.py", "validate")
        self.assertIn("3 events", result.stdout)
        self.target(target, "tools/validate_core_pin.py")
        self.assertIn(
            "--metadata-file",
            (target / "docs/agent_orchestration.md").read_text(),
        )

    def test_pin_tamper_path_duplicate_wrong_commit_and_source_tamper(self):
        managed_tamper = self.bootstrap("generic", "managed-tamper")
        (managed_tamper / "README.md").write_text("tampered", encoding="utf-8")
        self.target(
            managed_tamper, "tools/validate_core_pin.py", expected=2
        )

        bad_path = self.bootstrap("generic", "bad-path")
        lock_path = bad_path / "orchestration.lock.json"
        lock = json.loads(lock_path.read_text())
        lock["managed_files"][0]["target_path"] = (
            Path("..") / "outside.txt"
        ).as_posix()
        lock_path.write_text(json.dumps(lock), encoding="utf-8")
        self.target(bad_path, "tools/validate_core_pin.py", expected=2)

        duplicate = self.bootstrap("generic", "duplicate")
        lock_path = duplicate / "orchestration.lock.json"
        lock = json.loads(lock_path.read_text())
        lock["managed_files"][-1] = copy.deepcopy(lock["managed_files"][0])
        lock_path.write_text(json.dumps(lock), encoding="utf-8")
        self.target(duplicate, "tools/validate_core_pin.py", expected=2)

        missing = self.bootstrap("generic", "missing")
        lock_path = missing / "orchestration.lock.json"
        lock = json.loads(lock_path.read_text())
        lock["managed_files"].pop()
        lock_path.write_text(json.dumps(lock), encoding="utf-8")
        self.target(missing, "tools/validate_core_pin.py", expected=2)

        extra = self.bootstrap("generic", "extra")
        lock_path = extra / "orchestration.lock.json"
        lock = json.loads(lock_path.read_text())
        seed = copy.deepcopy(lock["managed_files"][0])
        seed["target_path"] = "extra-managed.txt"
        seed["core_path"] = "templates/base/extra-managed.txt"
        lock["managed_files"].append(seed)
        lock_path.write_text(json.dumps(lock), encoding="utf-8")
        self.target(extra, "tools/validate_core_pin.py", expected=2)

        nonhex = self.bootstrap("generic", "nonhex")
        lock_path = nonhex / "orchestration.lock.json"
        lock = json.loads(lock_path.read_text())
        lock["managed_files"][0]["target_sha256"] = "z" * 64
        lock_path.write_text(json.dumps(lock), encoding="utf-8")
        self.target(nonhex, "tools/validate_core_pin.py", expected=2)

        wrong_commit = self.bootstrap("generic", "wrong-commit")
        lock_path = wrong_commit / "orchestration.lock.json"
        lock = json.loads(lock_path.read_text())
        lock["core_commit"] = "0" * 40
        lock_path.write_text(json.dumps(lock), encoding="utf-8")
        self.target(
            wrong_commit,
            "tools/validate_core_pin.py",
            "--core-root",
            str(self.snapshot),
            expected=2,
        )

        source_tamper = self.bootstrap("generic", "source-tamper")
        (self.snapshot / "templates/base/README.md").write_text(
            "source tamper", encoding="utf-8"
        )
        self.target(
            source_tamper,
            "tools/validate_core_pin.py",
            "--core-root",
            str(self.snapshot),
            expected=2,
        )

    def make_symlink(self, link, target, directory=False):
        try:
            link.symlink_to(target, target_is_directory=directory)
        except (OSError, NotImplementedError) as exc:
            self.fail(f"symlink/reparse acceptance fixture unavailable: {exc}")

    def test_pin_rejects_symlink_file_and_parent(self):
        file_target = self.bootstrap("generic", "link-file")
        version = file_target / "VERSION"
        real = file_target / "VERSION.real"
        version.replace(real)
        self.make_symlink(version, real)
        self.target(file_target, "tools/validate_core_pin.py", expected=2)

        parent_target = self.bootstrap("generic", "link-parent")
        codex = parent_target / ".codex"
        real_codex = parent_target / ".codex.real"
        codex.replace(real_codex)
        self.make_symlink(codex, real_codex, directory=True)
        self.target(parent_target, "tools/validate_core_pin.py", expected=2)

    def test_mutable_target_and_core_boundaries(self):
        target = self.bootstrap("generic")
        (target / "PROJECT_LOG.md").write_text(
            "# Project Log\n\nMutable change.\n", encoding="utf-8"
        )
        with (target / "reports/agent_execution_ledger.jsonl").open(
            "a", encoding="utf-8"
        ) as handle:
            handle.write("")
        self.target(target, "tools/validate_core_pin.py")

        (self.snapshot / "PROJECT_LOG.md").write_text(
            "# Project Log\n\nMutable Core evidence changed.\n", encoding="utf-8"
        )
        self.core("tools/validate_orchestration.py")
        (self.snapshot / "templates/base/README.md").write_text(
            "managed template tamper", encoding="utf-8"
        )
        self.core("tools/validate_orchestration.py", expected=2)

    def test_sync_dry_run_no_mutation_and_apply_refusal(self):
        target = self.bootstrap("generic")
        before = {
            path.relative_to(target): path.read_bytes()
            for path in target.rglob("*")
            if path.is_file()
        }
        self.core("tools/sync_core.py", "--target", str(target))
        after = {
            path.relative_to(target): path.read_bytes()
            for path in target.rglob("*")
            if path.is_file()
        }
        self.assertEqual(before, after)
        self.core(
            "tools/sync_core.py",
            "--target",
            str(target),
            "--apply",
            expected=2,
        )
        final = {
            path.relative_to(target): path.read_bytes()
            for path in target.rglob("*")
            if path.is_file()
        }
        self.assertEqual(before, final)

    def test_bootstrap_has_no_large_inline_files_or_sibling_dependencies(self):
        source = (self.snapshot / "tools/bootstrap_project.py").read_text()
        self.assertLess(len(source), 20000)
        self.assertNotIn("write_text('#", source)
        self.assertNotIn("# Adapter Rules", source)
        for adapter_type in ("generic", "classical_ml"):
            target = self.bootstrap(adapter_type)
            for path in target.rglob("*"):
                if not path.is_file() or path.suffix == ".jsonl":
                    continue
                text = path.read_text(encoding="utf-8")
                self.assertNotIn(str(ROOT), text)
                self.assertNotIn(str(self.snapshot), text)
            self.target(target, "tools/validate_orchestration.py")


if __name__ == "__main__":
    unittest.main()
