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

## Later v1 gates

Prove managed-section sync against two adapters; require conflict detection,
clean-Git checks before writes, and human review before enabling `--apply`.
