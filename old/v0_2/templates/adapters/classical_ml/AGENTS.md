# Classical ML Adapter Rules

The root/main agent is supervisor-only. It reads `ML_PROJECT_ROADMAP.md`,
reports, the experiment ledger, checkpoint metadata, and Git state; defines
bounded worker scope and acceptance criteria; reviews evidence; and makes the
final continue/stop/change/freeze decision.

Workers perform code inspection and modification, routine investigation,
tests, benchmarks, data preparation, and approved ML runs. Use `luna_clerk`
with reasoning `none` only for deterministic clerical work, `terra_worker` at
`low` for default bounded work, and `sol_specialist` at `high` only after
explicit supervisor approval. Workers must not change model, reasoning, scope,
or delegate without approval.

Every repository task appends lifecycle events only through
`python tools/agent_ledger.py`; use `--metadata-file` for PowerShell starts.
Worker lifecycle events set `supervisor_decision` to `null`; only the
supervisor appends `reviewed`.

Before modelling, the supervisor must approve dataset identity, target,
license, leakage audit, and split strategy. `tools/experiment_ledger.py` is
mandatory for every material ML operation that actually runs. Record exact
commands, runtime, hashes, metrics, artifacts, and decision. Never fabricate
pending, skipped, or failed results and never rewrite JSONL history.

Long training and evaluation are semi-automatic and human-gated: a worker
prepares the exact command, the user launches it, and the worker does not
autonomously train, evaluate, or wait. Do not record secrets or commit
datasets, models, caches, outputs, checkpoints, or large artifacts.
