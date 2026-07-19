"""Validate a self-contained generic or declared adapter."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_REQUIRED = {
    ".codex/config.toml",
    ".codex/agents/luna_clerk.toml",
    ".codex/agents/terra_worker.toml",
    ".codex/agents/sol_specialist.toml",
    ".gitattributes",
    ".gitignore",
    "AGENTS.md",
    "README.md",
    "VERSION",
    "PROJECT_LOG.md",
    "orchestration.lock.json",
    "core/managed_files.json",
    "core/orchestration_lock.schema.json",
    "core/task_spec.schema.json",
    "core/project_manifest.schema.json",
    "docs/agent_orchestration.md",
    "tools/agent_ledger.py",
    "tools/validate_core_pin.py",
    "tools/validate_orchestration.py",
    "reports/agent_execution_ledger.schema.json",
    "reports/agent_execution_ledger.jsonl",
}
CLASSICAL_REQUIRED = {
    "ML_PROJECT_ROADMAP.md",
    "docs/classical_ml_adapter.md",
    "tools/experiment_ledger.py",
    "reports/experiment_ledger.schema.json",
    "reports/experiment_ledger.jsonl",
    "tests/test_classical_contract.py",
}
PRIVATE_RE = re.compile(
    r"(?im)(?:[A-Z]:[\\/](?:Users|home|ML)[\\/]|/"
    + "home/"
    + r"|api[_-]?key\s*=|secret\s*=|token\s*=)"
)


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate(root: Path = ROOT) -> list[str]:
    root = root.absolute()
    errors: list[str] = []
    for relative in sorted(BASE_REQUIRED):
        if not (root / relative).is_file():
            errors.append(f"missing {relative}")
    if errors:
        return errors

    try:
        pin_module = _load_module(
            "target_validate_core_pin", root / "tools" / "validate_core_pin.py"
        )
        lock = pin_module.validate_pin(root=root)
    except Exception as exc:
        errors.append(f"Core pin: {exc}")
        return errors

    adapter_type = lock["adapter_type"]
    if adapter_type == "classical_ml":
        if (root / "PROJECT_ROADMAP.md").exists():
            errors.append("classical adapter contains generic PROJECT_ROADMAP.md")
        for relative in sorted(CLASSICAL_REQUIRED):
            if not (root / relative).is_file():
                errors.append(f"missing {relative}")
    elif adapter_type == "generic":
        if not (root / "PROJECT_ROADMAP.md").is_file():
            errors.append("missing PROJECT_ROADMAP.md")
        for relative in sorted(CLASSICAL_REQUIRED):
            if (root / relative).exists():
                errors.append(f"generic adapter contains classical file {relative}")
    else:
        errors.append(f"unknown adapter_type {adapter_type}")

    for path in [
        root / ".codex" / "config.toml",
        *sorted((root / ".codex" / "agents").glob("*.toml")),
    ]:
        try:
            tomllib.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"TOML {path.relative_to(root)}: {exc}")

    schemas = [
        "reports/agent_execution_ledger.schema.json",
        "core/task_spec.schema.json",
        "core/project_manifest.schema.json",
        "core/orchestration_lock.schema.json",
    ]
    if adapter_type == "classical_ml":
        schemas.append("reports/experiment_ledger.schema.json")
    for relative in schemas:
        try:
            value = json.loads((root / relative).read_text(encoding="utf-8"))
            if not isinstance(value, dict) or value.get("type") != "object":
                raise ValueError("expected object schema")
        except Exception as exc:
            errors.append(f"schema {relative}: {exc}")

    try:
        agent = _load_module(
            "target_agent_ledger", root / "tools" / "agent_ledger.py"
        )
        prior = []
        for event in agent.read_events(
            root / "reports" / "agent_execution_ledger.jsonl"
        ):
            agent.validate(event)
            agent.lifecycle(prior, event)
            prior.append(event)
    except Exception as exc:
        errors.append(f"agent ledger: {exc}")

    if adapter_type == "classical_ml":
        try:
            experiment = _load_module(
                "target_experiment_ledger",
                root / "tools" / "experiment_ledger.py",
            )
            experiment.validate_ledger(
                root / "reports" / "experiment_ledger.jsonl",
                root=root,
            )
        except Exception as exc:
            errors.append(f"experiment ledger: {exc}")

    for path in root.rglob("*"):
        if (
            not path.is_file()
            or ".git" in path.parts
            or "__pycache__" in path.parts
            or path.suffix in {".pyc", ".jsonl"}
            or path.name == "orchestration.lock.json"
        ):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeError:
            continue
        if PRIVATE_RE.search(text):
            errors.append(f"private/absolute pattern in {path.relative_to(root)}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    errors = validate(args.root)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 2
    print("valid: orchestration adapter")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
