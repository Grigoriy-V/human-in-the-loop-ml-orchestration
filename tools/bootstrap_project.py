"""Create a self-contained adapter from canonical Core templates.

Official bootstrap is provenance-sensitive: the Core source must be a clean
Git checkout at an exact commit. Tests exercise the same path from an isolated
committed snapshot; there is no dirty-source bypass.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import uuid
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "templates" / "adapters.json"
CORE_REPOSITORY = "human-in-the-loop-ml-orchestration"
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
REPARSE_POINT = 0x400
REGISTRY_KEYS = {"schema_version", "adapters"}
ADAPTER_KEYS = {"managed_manifest", "mutable_files"}
MUTABLE_KEYS = {"target_path", "core_path", "mode"}
MANIFEST_KEYS = {"schema_version", "adapter_type", "files"}
MANAGED_KEYS = {"target_path", "core_path", "relationship"}


class BootstrapError(ValueError):
    """Bootstrap input, provenance, or template inventory is invalid."""


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _is_reparse(path: Path) -> bool:
    info = path.lstat()
    return path.is_symlink() or bool(
        getattr(info, "st_file_attributes", 0) & REPARSE_POINT
    )


def _relative(value: Any, field: str) -> PurePosixPath:
    if not isinstance(value, str) or not value or "\x00" in value:
        raise BootstrapError(f"{field} must be a non-empty relative path")
    if "\\" in value or ":" in value:
        raise BootstrapError(f"{field} must use canonical relative POSIX syntax")
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or value != path.as_posix()
        or any(part in {"", ".", ".."} for part in path.parts)
    ):
        raise BootstrapError(f"unsafe {field}: {value!r}")
    return path


def _source_file(value: str) -> Path:
    relative = _relative(value, "core_path")
    root = ROOT.absolute()
    if not root.is_dir() or _is_reparse(root):
        raise BootstrapError("Core root is missing or is a link/reparse point")
    current = root
    for part in relative.parts:
        current = current / part
        try:
            if _is_reparse(current):
                raise BootstrapError(
                    f"template path traverses a link/reparse point: {value}"
                )
        except FileNotFoundError as exc:
            raise BootstrapError(f"template source is missing: {value}") from exc
    try:
        resolved_root = root.resolve(strict=True)
        resolved = current.resolve(strict=True)
        resolved.relative_to(resolved_root)
    except (OSError, ValueError) as exc:
        raise BootstrapError(f"template source escapes Core: {value}") from exc
    if not stat.S_ISREG(resolved.stat().st_mode):
        raise BootstrapError(f"template source is not a regular file: {value}")
    return resolved


def _load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise BootstrapError(f"cannot read {label}: {exc}") from exc
    if not isinstance(value, dict):
        raise BootstrapError(f"{label} must be an object")
    return value


def _load_registry() -> dict[str, Any]:
    registry = _load_json(REGISTRY_PATH, "adapter registry")
    if set(registry) != REGISTRY_KEYS or registry["schema_version"] != "1.0":
        raise BootstrapError("adapter registry has an invalid closed shape")
    if not isinstance(registry["adapters"], dict) or not registry["adapters"]:
        raise BootstrapError("adapter registry must declare adapters")
    for adapter_type, config in registry["adapters"].items():
        if not isinstance(adapter_type, str) or not adapter_type:
            raise BootstrapError("adapter registry contains an invalid name")
        if not isinstance(config, dict) or set(config) != ADAPTER_KEYS:
            raise BootstrapError(f"invalid closed registry entry: {adapter_type}")
        _relative(config["managed_manifest"], "managed_manifest")
        if not isinstance(config["mutable_files"], list):
            raise BootstrapError("mutable_files must be an array")
        for entry in config["mutable_files"]:
            if not isinstance(entry, dict) or set(entry) != MUTABLE_KEYS:
                raise BootstrapError("mutable file entry must be closed")
            _relative(entry["target_path"], "target_path")
            if entry["mode"] == "copy":
                _relative(entry["core_path"], "core_path")
            elif entry["mode"] == "empty":
                if entry["core_path"] is not None:
                    raise BootstrapError("empty mutable file requires core_path null")
            else:
                raise BootstrapError("mutable file mode must be copy or empty")
    return registry


def _load_managed_manifest(
    adapter_type: str, config: dict[str, Any]
) -> dict[str, Any]:
    source = _source_file(config["managed_manifest"])
    manifest = _load_json(source, "managed-file manifest")
    if (
        set(manifest) != MANIFEST_KEYS
        or manifest["schema_version"] != "1.0"
        or manifest["adapter_type"] != adapter_type
        or not isinstance(manifest["files"], list)
        or not manifest["files"]
    ):
        raise BootstrapError("managed-file manifest has an invalid closed shape")
    targets: set[str] = set()
    sources: set[str] = set()
    for entry in manifest["files"]:
        if not isinstance(entry, dict) or set(entry) != MANAGED_KEYS:
            raise BootstrapError("managed-file entry must be a closed object")
        target_path = str(_relative(entry["target_path"], "target_path"))
        core_path = str(_relative(entry["core_path"], "core_path"))
        relationship = entry["relationship"]
        if relationship == "base_copy":
            expected_prefix = "templates/base/"
        elif relationship == "overlay_copy":
            expected_prefix = f"templates/adapters/{adapter_type}/"
        else:
            raise BootstrapError(f"unsupported relationship: {relationship}")
        if not core_path.startswith(expected_prefix):
            raise BootstrapError(
                f"{relationship} source is outside its declared boundary: {core_path}"
            )
        if target_path in targets or core_path in sources:
            raise BootstrapError("managed target and Core paths must be unique")
        targets.add(target_path)
        sources.add(core_path)
        _source_file(core_path)
    manifest_target = "core/managed_files.json"
    if manifest_target not in targets:
        raise BootstrapError("managed manifest must cover itself")
    return manifest


def _git_provenance() -> str:
    try:
        status = subprocess.run(
            [
                "git",
                "-C",
                os.fspath(ROOT),
                "status",
                "--porcelain=v1",
                "--untracked-files=all",
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=15,
        ).stdout
        commit = subprocess.run(
            ["git", "-C", os.fspath(ROOT), "rev-parse", "--verify", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            timeout=15,
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError) as exc:
        raise BootstrapError(f"cannot establish Core Git provenance: {exc}") from exc
    if status:
        raise BootstrapError("official bootstrap requires a clean Core checkout")
    if not COMMIT_RE.fullmatch(commit):
        raise BootstrapError("Core HEAD must be an exact lowercase 40-hex commit")
    return commit


def _copy(source: Path, destination: Path) -> None:
    """Copy without decoding; managed callers verify exact byte equality."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def _safe_cleanup(path: Path, parent: Path) -> None:
    try:
        path.absolute().relative_to(parent.absolute())
    except ValueError as exc:
        raise BootstrapError("refusing unsafe temporary cleanup") from exc
    if path.exists():
        shutil.rmtree(path)


def bootstrap(
    *,
    target: Path,
    adapter_type: str,
    adapter_name: str,
    dry_run: bool = False,
) -> dict[str, Any]:
    registry = _load_registry()
    if adapter_type not in registry["adapters"]:
        raise BootstrapError(
            f"unknown adapter_type {adapter_type!r}; "
            f"declared={sorted(registry['adapters'])}"
        )
    if (
        not isinstance(adapter_name, str)
        or not adapter_name.strip()
        or len(adapter_name) > 128
        or any(ord(char) < 32 for char in adapter_name)
    ):
        raise BootstrapError("adapter_name must be a non-empty printable string")
    target = target.absolute()
    if target.exists():
        raise BootstrapError("target must not already exist")
    if not target.parent.is_dir() or _is_reparse(target.parent):
        raise BootstrapError("target parent must be an existing regular directory")

    commit = _git_provenance()
    version = _source_file("VERSION").read_text(encoding="utf-8").strip()
    if version != "0.2.0":
        raise BootstrapError("bootstrap source VERSION must be 0.2.0")
    config = registry["adapters"][adapter_type]
    managed = _load_managed_manifest(adapter_type, config)

    mutable_targets: set[str] = set()
    for entry in config["mutable_files"]:
        target_path = str(_relative(entry["target_path"], "target_path"))
        if target_path in mutable_targets:
            raise BootstrapError(f"duplicate mutable target: {target_path}")
        mutable_targets.add(target_path)
        if entry["mode"] == "copy":
            _source_file(entry["core_path"])
    managed_targets = {entry["target_path"] for entry in managed["files"]}
    if managed_targets & mutable_targets:
        raise BootstrapError("managed and mutable target inventories overlap")

    if dry_run:
        return {
            "adapter_type": adapter_type,
            "managed_count": len(managed["files"]),
            "mutable_count": len(config["mutable_files"]),
            "core_commit": commit,
            "dry_run": True,
        }

    temporary = target.parent / f".{target.name}.bootstrap-{uuid.uuid4().hex}"
    try:
        temporary.mkdir()
        pin_entries: list[dict[str, str]] = []
        for entry in managed["files"]:
            source = _source_file(entry["core_path"])
            destination = temporary / PurePosixPath(entry["target_path"])
            _copy(source, destination)
            source_hash = _sha256(source)
            target_hash = _sha256(destination)
            if source_hash != target_hash:
                raise BootstrapError(
                    f"copy hash mismatch for {entry['target_path']}"
                )
            pin_entries.append(
                {
                    "target_path": entry["target_path"],
                    "target_sha256": target_hash,
                    "core_path": entry["core_path"],
                    "core_sha256": source_hash,
                    "relationship": entry["relationship"],
                }
            )
        for entry in config["mutable_files"]:
            destination = temporary / PurePosixPath(entry["target_path"])
            destination.parent.mkdir(parents=True, exist_ok=True)
            if entry["mode"] == "copy":
                _copy(_source_file(entry["core_path"]), destination)
            else:
                destination.write_bytes(b"")

        lock = {
            "schema_version": "1.0",
            "core_repository": CORE_REPOSITORY,
            "core_version": version,
            "core_commit": commit,
            "adapter_type": adapter_type,
            "adapter_name": adapter_name,
            "managed_manifest": "core/managed_files.json",
            "managed_files": pin_entries,
        }
        (temporary / "orchestration.lock.json").write_text(
            json.dumps(lock, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        validation = subprocess.run(
            [sys.executable, "tools/validate_core_pin.py"],
            cwd=temporary,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if validation.returncode:
            raise BootstrapError(
                "emitted adapter failed local pin validation: "
                f"{validation.stderr or validation.stdout}"
            )
        temporary.replace(target)
    except Exception:
        _safe_cleanup(temporary, target.parent)
        raise

    return {
        "adapter_type": adapter_type,
        "managed_count": len(managed["files"]),
        "mutable_count": len(config["mutable_files"]),
        "core_commit": commit,
        "dry_run": False,
        "target": os.fspath(target),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--adapter-type", required=True)
    parser.add_argument("--adapter-name", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = bootstrap(
            target=args.target,
            adapter_type=args.adapter_type,
            adapter_name=args.adapter_name,
            dry_run=args.dry_run,
        )
    except (BootstrapError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
