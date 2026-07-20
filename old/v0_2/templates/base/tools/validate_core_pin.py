"""Validate a bootstrapped adapter's immutable Core provenance."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / "orchestration.lock.json"
CORE_REPOSITORY = "human-in-the-loop-ml-orchestration"
SUPPORTED_ADAPTERS = {"generic", "classical_ml"}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
VERSION_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
REPARSE_POINT = 0x400
LOCK_KEYS = {
    "schema_version",
    "core_repository",
    "core_version",
    "core_commit",
    "adapter_type",
    "adapter_name",
    "managed_manifest",
    "managed_files",
}
LOCK_ENTRY_KEYS = {
    "target_path",
    "target_sha256",
    "core_path",
    "core_sha256",
    "relationship",
}
MANIFEST_KEYS = {"schema_version", "adapter_type", "files"}
MANIFEST_ENTRY_KEYS = {"target_path", "core_path", "relationship"}


class PinError(ValueError):
    """The Core pin or a managed file is invalid."""


def sha256_file(path: Path) -> str:
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
        raise PinError(f"{field} must be a non-empty relative path")
    if "\\" in value or ":" in value:
        raise PinError(f"{field} must use canonical repository-relative POSIX syntax")
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or value != path.as_posix()
        or any(part in {"", ".", ".."} for part in path.parts)
    ):
        raise PinError(f"unsafe {field}: {value!r}")
    return path


def _regular_contained(root: Path, value: str, field: str) -> Path:
    relative = _relative(value, field)
    root = root.absolute()
    if not root.is_dir() or _is_reparse(root):
        raise PinError(f"{field} root is missing or is a link/reparse point")
    current = root
    for part in relative.parts:
        current = current / part
        try:
            if _is_reparse(current):
                raise PinError(f"{field} traverses a link/reparse point: {value}")
        except FileNotFoundError as exc:
            raise PinError(f"{field} is missing: {value}") from exc
    try:
        resolved_root = root.resolve(strict=True)
        resolved = current.resolve(strict=True)
        resolved.relative_to(resolved_root)
    except (OSError, ValueError) as exc:
        raise PinError(f"{field} escapes its repository: {value}") from exc
    if not stat.S_ISREG(resolved.stat().st_mode):
        raise PinError(f"{field} is not a regular file: {value}")
    return resolved


def _load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise PinError(f"cannot read {label}: {exc}") from exc
    if not isinstance(value, dict):
        raise PinError(f"{label} must be an object")
    return value


def _load_lock(path: Path) -> dict[str, Any]:
    lock = _load_json(path, "Core pin")
    if set(lock) != LOCK_KEYS:
        raise PinError("Core pin must be a closed object")
    if lock["schema_version"] != "1.0":
        raise PinError("unsupported Core pin schema_version")
    if lock["core_repository"] != CORE_REPOSITORY:
        raise PinError("unexpected Core repository identity")
    if not isinstance(lock["core_version"], str) or not VERSION_RE.fullmatch(
        lock["core_version"]
    ):
        raise PinError("core_version must be semantic x.y.z")
    if not isinstance(lock["core_commit"], str) or not COMMIT_RE.fullmatch(
        lock["core_commit"]
    ):
        raise PinError("core_commit must be lowercase 40-hex")
    if lock["adapter_type"] not in SUPPORTED_ADAPTERS:
        raise PinError("adapter_type is not supported")
    if not isinstance(lock["adapter_name"], str) or not lock["adapter_name"].strip():
        raise PinError("adapter_name must be non-empty")
    if lock["managed_manifest"] != "core/managed_files.json":
        raise PinError("managed_manifest must use the canonical target path")
    if not isinstance(lock["managed_files"], list) or not lock["managed_files"]:
        raise PinError("managed_files must be a non-empty array")
    return lock


def _load_manifest(root: Path, adapter_type: str) -> dict[str, Any]:
    path = _regular_contained(
        root, "core/managed_files.json", "managed_manifest"
    )
    manifest = _load_json(path, "managed-file manifest")
    if (
        set(manifest) != MANIFEST_KEYS
        or manifest["schema_version"] != "1.0"
        or manifest["adapter_type"] != adapter_type
        or not isinstance(manifest["files"], list)
        or not manifest["files"]
    ):
        raise PinError("managed-file manifest has an invalid closed shape")
    return manifest


def _manifest_map(
    manifest: dict[str, Any], adapter_type: str
) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    sources: set[str] = set()
    for entry in manifest["files"]:
        if not isinstance(entry, dict) or set(entry) != MANIFEST_ENTRY_KEYS:
            raise PinError("managed manifest entries must be closed objects")
        target = str(_relative(entry["target_path"], "target_path"))
        source = str(_relative(entry["core_path"], "core_path"))
        relationship = entry["relationship"]
        if relationship == "base_copy":
            expected_prefix = "templates/base/"
        elif relationship == "overlay_copy":
            expected_prefix = f"templates/adapters/{adapter_type}/"
        else:
            raise PinError(f"unsupported relationship: {relationship}")
        if not source.startswith(expected_prefix):
            raise PinError(f"source violates {relationship} boundary: {source}")
        if target in result or source in sources:
            raise PinError("managed manifest paths must be unique")
        result[target] = entry
        sources.add(source)
    if "core/managed_files.json" not in result:
        raise PinError("managed manifest must cover itself")
    return result


def _lock_map(lock: dict[str, Any]) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    sources: set[str] = set()
    for entry in lock["managed_files"]:
        if not isinstance(entry, dict) or set(entry) != LOCK_ENTRY_KEYS:
            raise PinError("managed pin entries must be closed objects")
        target = str(_relative(entry["target_path"], "target_path"))
        source = str(_relative(entry["core_path"], "core_path"))
        if target in result or source in sources:
            raise PinError("managed pin paths must be unique")
        for field in ("target_sha256", "core_sha256"):
            if not isinstance(entry[field], str) or not SHA256_RE.fullmatch(
                entry[field]
            ):
                raise PinError(f"{field} must be lowercase SHA-256")
        if entry["relationship"] not in {"base_copy", "overlay_copy"}:
            raise PinError("unsupported managed relationship")
        if entry["target_sha256"] != entry["core_sha256"]:
            raise PinError("copy relationships require equal target/Core hashes")
        result[target] = entry
        sources.add(source)
    return result


def validate_pin(
    *,
    root: Path = ROOT,
    lock_path: Path | None = None,
    core_root: Path | None = None,
) -> dict[str, Any]:
    root = root.absolute()
    if lock_path is None:
        verified_lock = _regular_contained(
            root, "orchestration.lock.json", "Core pin"
        )
    else:
        lock_path = lock_path.absolute()
        try:
            relative_lock = lock_path.relative_to(root).as_posix()
        except ValueError as exc:
            raise PinError("Core pin path must stay inside the target") from exc
        verified_lock = _regular_contained(root, relative_lock, "Core pin")
    lock = _load_lock(verified_lock)
    manifest = _load_manifest(root, lock["adapter_type"])
    declared = _manifest_map(manifest, lock["adapter_type"])
    pinned = _lock_map(lock)
    if set(declared) != set(pinned):
        missing = sorted(set(declared) - set(pinned))
        extra = sorted(set(pinned) - set(declared))
        raise PinError(f"managed coverage mismatch; missing={missing}; extra={extra}")

    for target_path, declaration in declared.items():
        entry = pinned[target_path]
        if (
            entry["core_path"] != declaration["core_path"]
            or entry["relationship"] != declaration["relationship"]
        ):
            raise PinError(f"managed relationship mismatch: {target_path}")
        target_file = _regular_contained(root, target_path, "target_path")
        if sha256_file(target_file) != entry["target_sha256"]:
            raise PinError(f"target hash mismatch: {target_path}")

    version = _regular_contained(root, "VERSION", "target VERSION")
    if version.read_text(encoding="utf-8").strip() != lock["core_version"]:
        raise PinError("target VERSION does not match the Core pin")

    if core_root is not None:
        core_root = core_root.absolute()
        core_version = _regular_contained(core_root, "VERSION", "Core VERSION")
        if core_version.read_text(encoding="utf-8").strip() != lock["core_version"]:
            raise PinError("Core VERSION does not match the pin")
        try:
            commit = subprocess.run(
                ["git", "-C", os.fspath(core_root), "rev-parse", "--verify", "HEAD"],
                check=True,
                capture_output=True,
                text=True,
                timeout=15,
            ).stdout.strip()
        except (OSError, subprocess.SubprocessError) as exc:
            raise PinError(f"cannot verify Core Git commit: {exc}") from exc
        if commit != lock["core_commit"]:
            raise PinError("Core Git commit does not match the pin")
        for target_path, entry in pinned.items():
            source = _regular_contained(core_root, entry["core_path"], "core_path")
            if sha256_file(source) != entry["core_sha256"]:
                raise PinError(f"Core source hash mismatch: {target_path}")
    return lock


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--lock", type=Path)
    parser.add_argument("--core-root", type=Path)
    args = parser.parse_args(argv)
    try:
        lock = validate_pin(
            root=args.root,
            lock_path=args.lock,
            core_root=args.core_root,
        )
    except PinError as exc:
        print(f"error: invalid Core pin: {exc}", file=sys.stderr)
        return 2
    mode = "local+Core" if args.core_root else "local"
    print(
        f"valid: Core pin ({mode}, {lock['adapter_type']}, "
        f"{len(lock['managed_files'])} managed files)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
