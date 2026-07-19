# Orchestration Roadmap

## v0.1 — completed

Standalone Core: generic policies, safe ledger helper, schemas, local profiles,
bootstrap, dry-run-only sync, and no-GPU portability checks.

Acceptance requires a self-contained repository, clean initial ledger,
manifest validation, temporary adapter bootstrap and validation, and no source
project dependency.

Accepted in supervisor review. Next approved milestone: bootstrap a separate
classical-ML/sklearn adapter, then verify umbrella-supervisor behavior. This
closeout does not execute either action.

## Experimental boundary and possible future sync

v0.2 is a personal experimental proof of concept with nominal reproducibility,
not a production framework or v1.0.

Any future sync starts with a deterministic hash/diff over the declared
managed-file list. An agent is invoked only when differences exist, and any
proposed change requires manual approval. Automatic apply is out of scope.

## v0.2.0 candidate — accepted

Promote bootstrap inputs into canonical `templates/base` plus explicit
`generic` and `classical_ml` overlays. Emit exact clean-commit provenance,
closed managed manifests and target-local pin validation. Prove overlay
separation, mutable-boundary behavior, PowerShell metadata-file lifecycle,
audit-grade classical ledger behavior, and fail-closed negative paths from an
isolated committed Core snapshot.

The implementation and independent technical review were accepted in
supervisor events `5d407234-db43-484c-86e9-7d6d61884765` and
`5714c98f-e1d2-48c9-be15-46bdf9de05e3`.

The next milestone is a single supervisor acceptance and clean candidate
commit. This does not freeze v1.0. `sync_core.py --apply` remains unavailable.
