"""Validate Core v0.2 source, immutable manifest, and template boundaries."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
import sys
import tomllib
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CORE_REPOSITORY = "human-in-the-loop-ml-orchestration"
MUTABLE_BOUNDARIES = [
    "ORCHESTRATION_ROADMAP.md",
    "PROJECT_LOG.md",
    "reports/*.md",
    "reports/*.jsonl",
    "*.lock",
]
REQUIRED = {
    ".codex/config.toml",
    ".codex/agents/luna_clerk.toml",
    ".codex/agents/terra_worker.toml",
    ".codex/agents/sol_specialist.toml",
    ".gitignore",
    "AGENTS.md",
    "README.md",
    "VERSION",
    "ORCHESTRATION_ROADMAP.md",
    "PROJECT_LOG.md",
    "orchestration_manifest.json",
    "core/project_manifest.schema.json",
    "core/task_spec.schema.json",
    "core/orchestration_lock.schema.json",
    "templates/adapters.json",
    "templates/adapters/generic/core/managed_files.json",
    "templates/adapters/classical_ml/core/managed_files.json",
    "templates/base/tools/agent_ledger.py",
    "templates/base/tools/validate_core_pin.py",
    "templates/base/tools/validate_orchestration.py",
    "templates/adapters/classical_ml/tools/experiment_ledger.py",
    "reports/agent_execution_ledger.schema.json",
    "reports/agent_execution_ledger.jsonl",
    "tools/agent_ledger.py",
    "tools/bootstrap_project.py",
    "tools/sync_core.py",
    "tools/validate_orchestration.py",
}
PRIVATE_RE = re.compile(
    r"(?im)(?:[A-Z]:[\\/](?:Users|home|ML)[\\/]|/"
    + "home/"
    + r"|api[_-]?key\s*=|secret\s*=|token\s*=)"
)
REPARSE_POINT = 0x400


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _relative(value: Any, field: str) -> PurePosixPath:
    if not isinstance(value, str) or not value or "\x00" in value:
        raise ValueError(f"{field} must be a non-empty relative path")
    if "\\" in value or ":" in value:
        raise ValueError(f"{field} must use canonical POSIX syntax")
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or value != path.as_posix()
        or any(part in {"", ".", ".."} for part in path.parts)
    ):
        raise ValueError(f"unsafe {field}: {value!r}")
    return path


def _is_reparse(path: Path) -> bool:
    info = path.lstat()
    return path.is_symlink() or bool(
        getattr(info, "st_file_attributes", 0) & REPARSE_POINT
    )


def _regular_source(root: Path, value: str) -> Path:
    relative = _relative(value, "core_path")
    current = root
    for part in relative.parts:
        current = current / part
        if _is_reparse(current):
            raise ValueError(f"source traverses a link/reparse point: {value}")
    resolved = current.resolve(strict=True)
    resolved.relative_to(root.resolve(strict=True))
    if not stat.S_ISREG(resolved.stat().st_mode):
        raise ValueError(f"source is not a regular file: {value}")
    return resolved


def _is_mutable(relative: str) -> bool:
    path = PurePosixPath(relative)
    if relative in {"ORCHESTRATION_ROADMAP.md", "PROJECT_LOG.md"}:
        return True
    if len(path.parts) == 2 and path.parts[0] == "reports":
        return path.suffix in {".md", ".jsonl"}
    return relative.endswith(".lock")


def build_owned(root: Path) -> dict[str, str]:
    owned: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if (
            not path.is_file()
            or ".git" in path.parts
            or "__pycache__" in path.parts
            or path.suffix == ".pyc"
            or path.name == "orchestration_manifest.json"
        ):
            continue
        relative = path.relative_to(root).as_posix()
        if _is_mutable(relative):
            continue
        if _is_reparse(path):
            raise ValueError(f"owned file is a link/reparse point: {relative}")
        owned[relative] = digest(path)
    return owned


def _validate_templates(root: Path, errors: list[str]) -> None:
    try:
        registry = json.loads(
            (root / "templates" / "adapters.json").read_text(encoding="utf-8")
        )
        if set(registry) != {"schema_version", "adapters"}:
            raise ValueError("registry is not closed")
        if registry["schema_version"] != "1.0":
            raise ValueError("registry schema_version")
        if set(registry["adapters"]) != {"generic", "classical_ml"}:
            raise ValueError("registry must declare exactly generic and classical_ml")
        for adapter_type, config in registry["adapters"].items():
            if set(config) != {"managed_manifest", "mutable_files"}:
                raise ValueError(f"registry entry is not closed: {adapter_type}")
            manifest_path = _regular_source(root, config["managed_manifest"])
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            if (
                set(manifest) != {"schema_version", "adapter_type", "files"}
                or manifest["schema_version"] != "1.0"
                or manifest["adapter_type"] != adapter_type
            ):
                raise ValueError(f"managed manifest shape: {adapter_type}")
            targets: set[str] = set()
            sources: set[str] = set()
            for entry in manifest["files"]:
                if set(entry) != {"target_path", "core_path", "relationship"}:
                    raise ValueError(f"managed entry is not closed: {adapter_type}")
                target = str(_relative(entry["target_path"], "target_path"))
                source = str(_relative(entry["core_path"], "core_path"))
                relationship = entry["relationship"]
                prefix = (
                    "templates/base/"
                    if relationship == "base_copy"
                    else f"templates/adapters/{adapter_type}/"
                    if relationship == "overlay_copy"
                    else None
                )
                if prefix is None or not source.startswith(prefix):
                    raise ValueError(f"relationship boundary: {adapter_type}:{target}")
                if target in targets or source in sources:
                    raise ValueError(f"duplicate managed path: {adapter_type}")
                targets.add(target)
                sources.add(source)
                _regular_source(root, source)
            if "core/managed_files.json" not in targets:
                raise ValueError(f"manifest does not cover itself: {adapter_type}")
            mutable_targets: set[str] = set()
            for entry in config["mutable_files"]:
                if set(entry) != {"target_path", "core_path", "mode"}:
                    raise ValueError(f"mutable entry is not closed: {adapter_type}")
                target = str(_relative(entry["target_path"], "target_path"))
                if target in mutable_targets:
                    raise ValueError(f"duplicate mutable target: {adapter_type}")
                mutable_targets.add(target)
                if entry["mode"] == "copy":
                    _regular_source(root, entry["core_path"])
                elif entry["mode"] != "empty" or entry["core_path"] is not None:
                    raise ValueError(f"invalid mutable mode: {adapter_type}:{target}")
            if targets & mutable_targets:
                raise ValueError(f"managed/mutable overlap: {adapter_type}")
            classical_paths = {
                "ML_PROJECT_ROADMAP.md",
                "docs/classical_ml_adapter.md",
                "tools/experiment_ledger.py",
                "reports/experiment_ledger.schema.json",
                "reports/experiment_ledger.jsonl",
                "tests/test_classical_contract.py",
            }
            inventory = targets | mutable_targets
            if adapter_type == "generic" and inventory & classical_paths:
                raise ValueError("generic inventory leaks classical files")
            if adapter_type == "classical_ml" and not classical_paths <= inventory:
                raise ValueError("classical inventory is incomplete")
    except Exception as exc:
        errors.append(f"templates: {exc}")


def validate(root: Path = ROOT) -> list[str]:
    root = root.absolute()
    errors: list[str] = []
    for relative in sorted(REQUIRED):
        if not (root / relative).is_file():
            errors.append(f"missing {relative}")
    if errors:
        return errors
    try:
        version = (root / "VERSION").read_text(encoding="utf-8").strip()
        if version != "0.2.0":
            raise ValueError("VERSION must be 0.2.0")
        if (root / "templates/base/VERSION").read_text(encoding="utf-8").strip() != version:
            raise ValueError("base template VERSION differs")
    except Exception as exc:
        errors.append(f"version: {exc}")

    for path in [
        root / ".codex" / "config.toml",
        *sorted((root / ".codex" / "agents").glob("*.toml")),
        root / "templates" / "base" / ".codex" / "config.toml",
        *sorted((root / "templates" / "base" / ".codex" / "agents").glob("*.toml")),
    ]:
        try:
            tomllib.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"TOML {path.relative_to(root)}: {exc}")

    for path in root.rglob("*.json"):
        if ".git" in path.parts:
            continue
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(value, dict):
                raise ValueError("expected object")
        except Exception as exc:
            errors.append(f"JSON {path.relative_to(root)}: {exc}")

    try:
        sys.path.insert(0, str(root / "tools"))
        import agent_ledger
        prior = []
        for event in agent_ledger.read_events(
            root / "reports" / "agent_execution_ledger.jsonl"
        ):
            agent_ledger.validate(event)
            agent_ledger.lifecycle(prior, event)
            prior.append(event)
    except Exception as exc:
        errors.append(f"agent ledger: {exc}")

    _validate_templates(root, errors)
    try:
        manifest = json.loads(
            (root / "orchestration_manifest.json").read_text(encoding="utf-8")
        )
        if set(manifest) != {
            "core_repository",
            "core_version",
            "owned_files",
            "mutable_boundaries",
        }:
            raise ValueError("manifest is not a closed object")
        if manifest["core_repository"] != CORE_REPOSITORY:
            raise ValueError("Core repository identity")
        if manifest["core_version"] != "0.2.0":
            raise ValueError("Core manifest version")
        if manifest["mutable_boundaries"] != MUTABLE_BOUNDARIES:
            raise ValueError("mutable boundary declaration")
        if manifest["owned_files"] != build_owned(root):
            raise ValueError("immutable manifest hashes differ")
        for critical in (
            "tools/bootstrap_project.py",
            "tools/validate_orchestration.py",
            "templates/adapters.json",
            "templates/base/tools/validate_core_pin.py",
            "templates/adapters/classical_ml/tools/experiment_ledger.py",
        ):
            if critical not in manifest["owned_files"]:
                raise ValueError(f"manifest missing critical {critical}")
        if any(_is_mutable(path) for path in manifest["owned_files"]):
            raise ValueError("mutable file is incorrectly managed")
    except Exception as exc:
        errors.append(f"manifest: {exc}")

    for path in root.rglob("*"):
        if (
            not path.is_file()
            or ".git" in path.parts
            or "__pycache__" in path.parts
            or path.suffix in {".pyc", ".jsonl"}
            or (len(path.relative_to(root).parts) == 2 and path.parts[-2] == "reports")
        ):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeError:
            continue
        if PRIVATE_RE.search(text):
            errors.append(f"private/absolute pattern: {path.relative_to(root)}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--write-manifest", action="store_true")
    args = parser.parse_args(argv)
    root = args.root.absolute()
    if args.write_manifest:
        manifest = {
            "core_repository": CORE_REPOSITORY,
            "core_version": (root / "VERSION").read_text(encoding="utf-8").strip(),
            "owned_files": build_owned(root),
            "mutable_boundaries": MUTABLE_BOUNDARIES,
        }
        (root / "orchestration_manifest.json").write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"wrote immutable manifest ({len(manifest['owned_files'])} files)")
        return 0
    errors = validate(root)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 2
    print("valid: orchestration Core v0.2 candidate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
