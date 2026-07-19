"""Audit-grade append-only ledger for the classical-ML adapter."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import socket
import stat
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "reports" / "experiment_ledger.jsonl"
SCHEMA_VERSION = "2.0"
OPERATIONS = ("dataset_audit", "baseline", "evaluation", "closeout")
STATUSES = ("completed", "failed", "skipped", "pending")
RANK = {name: index for index, name in enumerate(OPERATIONS)}
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
UUID4_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
)
TIME_RE = re.compile(
    r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}"
    r"(?:\.[0-9]{1,6})?Z$"
)
EXPERIMENT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{2,127}$")
CLASS_RE = re.compile(
    r"^[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)+$"
)
REPARSE_POINT = 0x400
FULL_KEYS = {
    "schema_version",
    "event_id",
    "timestamp_utc",
    "experiment_id",
    "operation",
    "status",
    "commands",
    "runtime",
    "dataset",
    "leakage_audit",
    "split",
    "features",
    "pipeline",
    "baseline_cv",
    "calibration",
    "threshold",
    "artifacts",
    "decision",
}
CALLER_KEYS = FULL_KEYS - {"event_id", "timestamp_utc"}


class LedgerError(ValueError):
    """The experiment record or lifecycle is invalid."""


Error = LedgerError


def system_utc() -> str:
    return (
        datetime.now(timezone.utc)
        .isoformat(timespec="microseconds")
        .replace("+00:00", "Z")
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _closed(value: Any, keys: set[str], name: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != keys:
        raise LedgerError(f"{name} must be a closed object with {sorted(keys)}")
    return value


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise LedgerError(f"{name} must be a non-empty string")
    if value.strip().lower() in {"unknown", "pending", "placeholder", "n/a", "none"}:
        raise LedgerError(f"{name} must not be a placeholder")
    return value


def _strings(value: Any, name: str, *, required: bool = False) -> list[str]:
    if not isinstance(value, list) or (required and not value):
        raise LedgerError(f"{name} must be {'a non-empty ' if required else 'an '}array")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        raise LedgerError(f"{name} entries must be non-empty strings")
    if len(value) != len(set(value)):
        raise LedgerError(f"{name} entries must be unique")
    return value


def _number(value: Any, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise LedgerError(f"{name} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise LedgerError(f"{name} must be finite")
    return result


def _json_value(value: Any, name: str) -> None:
    if value is None or isinstance(value, (str, bool, int)):
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise LedgerError(f"{name} contains a non-finite number")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _json_value(item, f"{name}[{index}]")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str) or not key:
                raise LedgerError(f"{name} contains an invalid key")
            _json_value(item, f"{name}.{key}")
        return
    raise LedgerError(f"{name} contains a non-JSON value")


def _time(value: Any) -> datetime:
    if not isinstance(value, str) or not TIME_RE.fullmatch(value):
        raise LedgerError("timestamp_utc must be an exact UTC timestamp ending in Z")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise LedgerError("timestamp_utc is not a real calendar timestamp") from exc
    if parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        raise LedgerError("timestamp_utc must be UTC")
    return parsed


def _runtime(value: Any) -> dict[str, Any]:
    value = _closed(
        value, {"python_version", "platform", "executor", "packages"}, "runtime"
    )
    for field in ("python_version", "platform", "executor"):
        _text(value[field], f"runtime.{field}")
    if not isinstance(value["packages"], dict) or not value["packages"]:
        raise LedgerError("runtime.packages must be a non-empty object")
    for package, version in value["packages"].items():
        _text(package, "runtime package")
        _text(version, f"runtime.packages.{package}")
    return value


def _dataset(value: Any) -> dict[str, Any]:
    value = _closed(
        value,
        {"name", "source", "license", "fingerprint_sha256", "target"},
        "dataset",
    )
    for field in ("name", "source", "license"):
        _text(value[field], f"dataset.{field}")
    if not isinstance(value["fingerprint_sha256"], str) or not SHA_RE.fullmatch(
        value["fingerprint_sha256"]
    ):
        raise LedgerError("dataset fingerprint must be lowercase SHA-256")
    target = _closed(
        value["target"],
        {"column", "task_type", "positive_class"},
        "dataset.target",
    )
    _text(target["column"], "dataset.target.column")
    if target["task_type"] != "binary_classification":
        raise LedgerError("target task_type must be binary_classification")
    positive = target["positive_class"]
    if isinstance(positive, bool) or not isinstance(positive, (str, int)):
        raise LedgerError("positive_class must be a string or integer")
    if isinstance(positive, str):
        _text(positive, "positive_class")
    return value


def _leakage(value: Any, target: str) -> None:
    value = _closed(
        value,
        {"checked", "methods", "findings", "prohibited_features"},
        "leakage_audit",
    )
    if value["checked"] is not True:
        raise LedgerError("leakage_audit.checked must be true")
    _strings(value["methods"], "leakage methods", required=True)
    _strings(value["findings"], "leakage findings")
    prohibited = _strings(
        value["prohibited_features"], "prohibited features", required=True
    )
    if target not in prohibited:
        raise LedgerError("target must be prohibited as a feature")


def _split(value: Any, target: str) -> None:
    value = _closed(
        value,
        {
            "strategy",
            "random_state",
            "stratified",
            "stratify_by",
            "train_fingerprint_sha256",
            "test_fingerprint_sha256",
        },
        "split",
    )
    if value["strategy"] not in {"random", "temporal", "group"}:
        raise LedgerError("split strategy is unsupported")
    random_state = value["random_state"]
    if value["strategy"] == "random":
        if isinstance(random_state, bool) or not isinstance(random_state, int):
            raise LedgerError("random split requires integer random_state")
    elif random_state is not None:
        raise LedgerError("non-random split requires random_state null")
    if not isinstance(value["stratified"], bool):
        raise LedgerError("stratified must be boolean")
    if value["stratified"] and value["stratify_by"] != target:
        raise LedgerError("stratified split must use target")
    if not value["stratified"] and value["stratify_by"] is not None:
        raise LedgerError("non-stratified split requires stratify_by null")
    fingerprints = (
        value["train_fingerprint_sha256"],
        value["test_fingerprint_sha256"],
    )
    if any(not isinstance(item, str) or not SHA_RE.fullmatch(item) for item in fingerprints):
        raise LedgerError("split fingerprints must be lowercase SHA-256")
    if fingerprints[0] == fingerprints[1]:
        raise LedgerError("train and test fingerprints must differ")


def _features(value: Any, target: str) -> None:
    value = _closed(
        value, {"included", "categorical", "numeric", "excluded"}, "features"
    )
    included = _strings(value["included"], "included features", required=True)
    categorical = _strings(value["categorical"], "categorical features")
    numeric = _strings(value["numeric"], "numeric features")
    excluded = _strings(value["excluded"], "excluded features", required=True)
    if set(categorical) & set(numeric):
        raise LedgerError("categorical and numeric features overlap")
    if set(categorical) | set(numeric) != set(included):
        raise LedgerError("feature types must partition included features")
    if target in included or target not in excluded:
        raise LedgerError("target must be excluded from model features")


def _pipeline(value: Any) -> dict[str, Any]:
    value = _closed(value, {"library", "class", "steps"}, "pipeline")
    if value["library"] != "sklearn" or value["class"] != "sklearn.pipeline.Pipeline":
        raise LedgerError("pipeline must be sklearn.pipeline.Pipeline")
    if not isinstance(value["steps"], list) or len(value["steps"]) < 2:
        raise LedgerError("pipeline requires preprocessing and estimator steps")
    names: set[str] = set()
    for index, step in enumerate(value["steps"]):
        step = _closed(step, {"name", "class", "params"}, f"pipeline step {index}")
        name = _text(step["name"], "pipeline step name")
        if name in names:
            raise LedgerError("pipeline step names must be unique")
        names.add(name)
        if not isinstance(step["class"], str) or not CLASS_RE.fullmatch(step["class"]):
            raise LedgerError("pipeline step class must be fully qualified")
        if not isinstance(step["params"], dict) or not step["params"]:
            raise LedgerError("pipeline step params must be non-empty")
        _json_value(step["params"], "pipeline params")
    return value


def _metrics(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, dict) or not value:
        raise LedgerError(f"{name} must be a non-empty object")
    for metric, score in value.items():
        _text(metric, f"{name} metric")
        _number(score, f"{name}.{metric}")
    return value


def _baseline(value: Any, pipeline: dict[str, Any]) -> None:
    value = _closed(
        value, {"baseline_model", "cv", "metrics", "primary_metric"}, "baseline_cv"
    )
    model = _closed(
        value["baseline_model"], {"class", "params"}, "baseline model"
    )
    if not isinstance(model["class"], str) or not CLASS_RE.fullmatch(model["class"]):
        raise LedgerError("baseline model class must be fully qualified")
    if model["class"] != pipeline["steps"][-1]["class"]:
        raise LedgerError("baseline model must match final Pipeline estimator")
    if not isinstance(model["params"], dict) or not model["params"]:
        raise LedgerError("baseline model params must be non-empty")
    _json_value(model["params"], "baseline model params")
    cv = _closed(
        value["cv"], {"strategy", "folds", "shuffle", "random_state"}, "CV"
    )
    if cv["strategy"] not in {"StratifiedKFold", "GroupKFold", "TimeSeriesSplit"}:
        raise LedgerError("CV strategy is unsupported")
    if isinstance(cv["folds"], bool) or not isinstance(cv["folds"], int) or not 2 <= cv["folds"] <= 20:
        raise LedgerError("CV folds must be 2..20")
    if not isinstance(cv["shuffle"], bool):
        raise LedgerError("CV shuffle must be boolean")
    if cv["shuffle"]:
        if isinstance(cv["random_state"], bool) or not isinstance(cv["random_state"], int):
            raise LedgerError("shuffled CV requires integer random_state")
    elif cv["random_state"] is not None:
        raise LedgerError("unshuffled CV requires random_state null")
    if cv["strategy"] in {"GroupKFold", "TimeSeriesSplit"} and cv["shuffle"]:
        raise LedgerError("group/time CV cannot shuffle")
    metrics = _metrics(value["metrics"], "baseline metrics")
    if value["primary_metric"] not in metrics:
        raise LedgerError("primary metric must be recorded")


def _calibration(value: Any) -> None:
    value = _closed(
        value, {"method", "cv_folds", "metrics_before", "metrics_after"}, "calibration"
    )
    if value["method"] not in {"sigmoid", "isotonic", "none"}:
        raise LedgerError("calibration method is unsupported")
    if isinstance(value["cv_folds"], bool) or not isinstance(value["cv_folds"], int) or not 2 <= value["cv_folds"] <= 20:
        raise LedgerError("calibration folds must be 2..20")
    _metrics(value["metrics_before"], "calibration metrics_before")
    _metrics(value["metrics_after"], "calibration metrics_after")


def _threshold(value: Any) -> None:
    value = _closed(
        value,
        {"value", "objective", "selection_split", "metric_name", "metric_value"},
        "threshold",
    )
    if not 0 <= _number(value["value"], "threshold.value") <= 1:
        raise LedgerError("threshold must be between 0 and 1")
    _text(value["objective"], "threshold objective")
    if value["selection_split"] not in {"validation", "train_cv_oof"}:
        raise LedgerError("threshold selection split is unsupported")
    _text(value["metric_name"], "threshold metric")
    _number(value["metric_value"], "threshold metric value")


def _is_reparse(path: Path) -> bool:
    info = path.lstat()
    return path.is_symlink() or bool(
        getattr(info, "st_file_attributes", 0) & REPARSE_POINT
    )


def _relative(value: Any, name: str) -> PurePosixPath:
    if not isinstance(value, str) or not value or "\x00" in value:
        raise LedgerError(f"{name} must be a non-empty relative path")
    if "\\" in value or ":" in value:
        raise LedgerError(f"{name} must use canonical relative POSIX syntax")
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or value != path.as_posix()
        or any(part in {"", ".", ".."} for part in path.parts)
    ):
        raise LedgerError(f"unsafe {name}: {value!r}")
    return path


def _regular_file(root: Path, value: str, name: str) -> Path:
    relative = _relative(value, name)
    root = root.absolute()
    if not root.is_dir() or _is_reparse(root):
        raise LedgerError("project root is missing or is a link/reparse point")
    current = root
    for part in relative.parts:
        current = current / part
        try:
            if _is_reparse(current):
                raise LedgerError(f"{name} traverses a link/reparse point")
        except FileNotFoundError as exc:
            raise LedgerError(f"{name} is missing") from exc
    try:
        resolved_root = root.resolve(strict=True)
        resolved = current.resolve(strict=True)
        resolved.relative_to(resolved_root)
    except (OSError, ValueError) as exc:
        raise LedgerError(f"{name} escapes the project") from exc
    if not stat.S_ISREG(resolved.stat().st_mode):
        raise LedgerError(f"{name} must be a regular file")
    return resolved


def _artifacts(value: Any, root: Path) -> None:
    if not isinstance(value, list):
        raise LedgerError("artifacts must be an array")
    seen: set[str] = set()
    for index, artifact in enumerate(value):
        artifact = _closed(artifact, {"path", "sha256"}, f"artifact {index}")
        if artifact["path"] in seen:
            raise LedgerError("artifact paths must be unique")
        seen.add(artifact["path"])
        if not isinstance(artifact["sha256"], str) or not SHA_RE.fullmatch(
            artifact["sha256"]
        ):
            raise LedgerError("artifact hash must be lowercase SHA-256")
        path = _regular_file(root, artifact["path"], "artifact path")
        if sha256_file(path) != artifact["sha256"]:
            raise LedgerError("artifact hash mismatch")


def _decision(value: Any, status: str) -> None:
    value = _closed(value, {"action", "rationale"}, "decision")
    actions = {
        "completed": {"continue", "stop", "change", "freeze"},
        "failed": {"stop", "change"},
        "skipped": {"stop", "change"},
        "pending": {"pending"},
    }
    if value["action"] not in actions[status]:
        raise LedgerError("decision action is invalid for status")
    _text(value["rationale"], "decision rationale")


def validate_event(event: Any, *, root: Path = ROOT) -> dict[str, Any]:
    event = _closed(event, FULL_KEYS, "event")
    if event["schema_version"] != SCHEMA_VERSION:
        raise LedgerError("schema_version must be 2.0")
    if not isinstance(event["event_id"], str) or not UUID4_RE.fullmatch(
        event["event_id"]
    ):
        raise LedgerError("event_id must be canonical UUIDv4")
    _time(event["timestamp_utc"])
    if not isinstance(event["experiment_id"], str) or not EXPERIMENT_RE.fullmatch(
        event["experiment_id"]
    ):
        raise LedgerError("experiment_id is invalid")
    if event["operation"] not in OPERATIONS or event["status"] not in STATUSES:
        raise LedgerError("operation/status is unsupported")
    commands = _strings(event["commands"], "commands")
    status = event["status"]
    operation = event["operation"]
    _decision(event["decision"], status)
    _artifacts(event["artifacts"], root)

    result_fields = (
        "dataset",
        "leakage_audit",
        "split",
        "features",
        "pipeline",
        "baseline_cv",
        "calibration",
        "threshold",
    )
    if status != "completed":
        if status == "failed":
            if not commands:
                raise LedgerError("failed event must record the failed command")
            _runtime(event["runtime"])
        elif commands or event["runtime"] is not None:
            raise LedgerError("pending/skipped cannot claim commands or runtime")
        if any(event[field] is not None for field in result_fields):
            raise LedgerError(f"{status} event cannot claim results")
        if event["artifacts"]:
            raise LedgerError(f"{status} event cannot claim artifacts")
        return event

    if not commands:
        raise LedgerError("completed event must record exact commands")
    _runtime(event["runtime"])
    data = _dataset(event["dataset"])
    target = data["target"]["column"]
    relevant: set[str]
    if operation == "dataset_audit":
        _leakage(event["leakage_audit"], target)
        _split(event["split"], target)
        _features(event["features"], target)
        relevant = {"leakage_audit", "split", "features"}
    elif operation == "baseline":
        pipe = _pipeline(event["pipeline"])
        _baseline(event["baseline_cv"], pipe)
        relevant = {"pipeline", "baseline_cv"}
    elif operation == "evaluation":
        pipe = _pipeline(event["pipeline"])
        _baseline(event["baseline_cv"], pipe)
        _calibration(event["calibration"])
        _threshold(event["threshold"])
        relevant = {"pipeline", "baseline_cv", "calibration", "threshold"}
    else:
        relevant = set()
    for field in set(result_fields) - {"dataset"} - relevant:
        if event[field] is not None:
            raise LedgerError(f"{operation} cannot claim irrelevant {field}")
    return event


def validate_sequence(events: list[dict[str, Any]]) -> None:
    ids: set[str] = set()
    previous_time: datetime | None = None
    states: dict[str, dict[str, Any]] = {}
    for event in events:
        if event["event_id"] in ids:
            raise LedgerError("duplicate event_id")
        ids.add(event["event_id"])
        current_time = _time(event["timestamp_utc"])
        if previous_time is not None and current_time <= previous_time:
            raise LedgerError("timestamps must be strictly increasing")
        previous_time = current_time
        state = states.setdefault(
            event["experiment_id"],
            {
                "dataset": None,
                "rank": -1,
                "statuses": {},
                "pending": None,
                "closed": False,
            },
        )
        if state["closed"]:
            raise LedgerError("event follows terminal closeout")
        operation = event["operation"]
        status = event["status"]
        rank = RANK[operation]
        if rank < state["rank"]:
            raise LedgerError("operation order regressed")
        if state["pending"] is not None and state["pending"] != operation:
            raise LedgerError("pending operation is unresolved")
        prior = state["statuses"].get(operation)
        if prior is not None and (prior != "pending" or status == "pending"):
            raise LedgerError("invalid repeated operation lifecycle")
        if operation == "baseline" and state["statuses"].get("dataset_audit") != "completed":
            raise LedgerError("baseline requires completed dataset audit")
        if operation == "evaluation" and state["statuses"].get("baseline") != "completed":
            raise LedgerError("evaluation requires completed baseline")
        if operation == "closeout":
            audit = state["statuses"].get("dataset_audit")
            if audit not in {"completed", "failed", "skipped"}:
                raise LedgerError("closeout requires terminal dataset audit")
            if status == "completed" and audit != "completed":
                raise LedgerError("completed closeout requires completed audit")
        if status == "completed":
            if state["dataset"] is None:
                state["dataset"] = event["dataset"]
            elif state["dataset"] != event["dataset"]:
                raise LedgerError("experiment identity drift")
        state["statuses"][operation] = status
        state["rank"] = max(state["rank"], rank)
        state["pending"] = operation if status == "pending" else None
        if operation == "closeout" and status in {"completed", "failed", "skipped"}:
            state["closed"] = True


def _parse(text: str, name: str) -> Any:
    def reject(value: str) -> None:
        raise LedgerError(f"{name} contains invalid JSON constant {value}")
    try:
        return json.loads(text, parse_constant=reject)
    except (json.JSONDecodeError, UnicodeError) as exc:
        raise LedgerError(f"{name} is not strict JSON: {exc}") from exc


def read_events(path: Path, *, root: Path = ROOT) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    try:
        raw = path.read_bytes()
        text = raw.decode("utf-8")
    except (OSError, UnicodeError) as exc:
        raise LedgerError(f"cannot read ledger: {exc}") from exc
    if not raw:
        return []
    if not raw.endswith(b"\n"):
        raise LedgerError("ledger must end with newline")
    events = []
    for number, line in enumerate(text.splitlines(), 1):
        if not line:
            raise LedgerError(f"blank line {number}")
        event = _parse(line, f"line {number}")
        try:
            validate_event(event, root=root)
        except LedgerError as exc:
            raise LedgerError(f"line {number}: {exc}") from exc
        events.append(event)
    validate_sequence(events)
    return events


def _ledger_location(path: Path, root: Path) -> tuple[Path, Path]:
    root = root.absolute()
    path = path.absolute()
    if not root.is_dir() or _is_reparse(root):
        raise LedgerError("project root is missing or linked")
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise LedgerError("ledger must stay inside project") from exc
    current = root
    for part in path.relative_to(root).parts[:-1]:
        current = current / part
        if not current.is_dir() or _is_reparse(current):
            raise LedgerError("ledger parent is missing or linked")
    if path.exists() and (_is_reparse(path) or not stat.S_ISREG(path.stat().st_mode)):
        raise LedgerError("ledger must be a regular non-link file")
    return path, Path(os.fspath(path) + ".lock")


def _caller(event: Any) -> dict[str, Any]:
    if not isinstance(event, dict):
        raise LedgerError("append payload must be an object")
    forbidden = {"event_id", "timestamp_utc"} & set(event)
    if forbidden:
        raise LedgerError(f"caller cannot supply {sorted(forbidden)}")
    if set(event) != CALLER_KEYS:
        raise LedgerError("append payload must use the exact closed field set")
    return event


def _lock(path: Path) -> int:
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise LedgerError("ledger lock exists; confirm no writer before removal") from exc
    metadata = json.dumps(
        {"pid": os.getpid(), "host": socket.gethostname(), "created_utc": system_utc()},
        separators=(",", ":"),
    ).encode()
    try:
        if os.write(fd, metadata) != len(metadata):
            raise OSError("short lock write")
        os.fsync(fd)
    except OSError:
        os.close(fd)
        try:
            path.unlink()
        except OSError:
            pass
        raise
    return fd


def _unlock(fd: int, path: Path) -> None:
    os.close(fd)
    path.unlink()


def append_event(
    event: dict[str, Any], path: Path = LEDGER, *, root: Path = ROOT
) -> dict[str, Any]:
    event = _caller(event)
    path, lock_path = _ledger_location(path, root)
    lock_fd = _lock(lock_path)
    write_started = False
    try:
        prior = read_events(path, root=root)
        complete = {
            **event,
            "event_id": str(uuid.uuid4()),
            "timestamp_utc": system_utc(),
        }
        validate_event(complete, root=root)
        validate_sequence([*prior, complete])
        record = (
            json.dumps(
                complete,
                ensure_ascii=False,
                allow_nan=False,
                separators=(",", ":"),
            )
            + "\n"
        ).encode()
        ledger_fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
        write_started = True
        try:
            if os.write(ledger_fd, record) != len(record):
                raise OSError("short ledger append")
            os.fsync(ledger_fd)
        finally:
            os.close(ledger_fd)
    except Exception:
        if write_started:
            os.close(lock_fd)
        else:
            _unlock(lock_fd, lock_path)
        raise
    _unlock(lock_fd, lock_path)
    return complete


append = append_event


def validate_ledger(path: Path = LEDGER, *, root: Path = ROOT):
    path, _ = _ledger_location(path, root)
    return read_events(path, root=root)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, default=LEDGER)
    parser.add_argument("--root", type=Path, default=ROOT)
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("append")
    source = add.add_mutually_exclusive_group(required=True)
    source.add_argument("--event-json")
    source.add_argument("--event-file", type=Path)
    commands.add_parser("validate")
    args = parser.parse_args(argv)
    try:
        if args.command == "append":
            text = (
                args.event_file.read_text(encoding="utf-8")
                if args.event_file
                else args.event_json
            )
            result = append_event(_parse(text, "payload"), args.ledger, root=args.root)
            print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
        else:
            events = validate_ledger(args.ledger, root=args.root)
            print(f"valid: experiment ledger ({len(events)} events)")
    except (LedgerError, OSError, UnicodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
