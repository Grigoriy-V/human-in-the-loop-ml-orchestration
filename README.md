# Human-in-the-Loop Orchestration Core

Core v0.1 is a small, project-local foundation for supervised agent work. It
provides a ledger, bounded task contract, routing profiles, validation, and a
safe bootstrap path. It is intentionally independent of any ML framework or
dataset.

## Boundaries

Core owns the generic lifecycle and its templates. A project adapter owns its
domain rules, data policy, experiments, reports, and decisions. A human
approves direction and any long-running or consequential operation.

## Quick validation (no GPU)

Python 3.11+ is required; Core v0.1 has no runtime dependencies. Run:

```powershell
python -m unittest discover -s tests -v
python tools/validate_orchestration.py
python tools/bootstrap_project.py --dry-run --target <empty-directory> --adapter-type example --adapter-name Example
```

For a Windows-safe first ledger append, put the start metadata JSON in a file
and run `python tools/agent_ledger.py start --metadata-file task-start.json`.
Avoid shell-embedded JSON: it is easy to quote incorrectly.

No GPU, dataset, training, evaluation, or network call is used.

## Limitations

v0.1 bootstrap is deliberately conservative. `sync_core.py` validates and
prints a dry-run only; it does not mutate adapters until a future release can
prove safe managed-section updates. It never commits or pushes.
