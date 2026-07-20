# Agent Operating Contract

## Human and execution

The human controls project direction. Discussion, questions, ideas, candidates,
and roadmap edits do not authorize implementation. Commands such as "start
work", "continue work", or "follow the plan" authorize execution of the
current agreed step within its existing boundaries and human gates.

## Roles and routing

- The main Sol agent is supervisor: it owns strategy, roadmap use, task design,
  routing, acceptance, and the final report. It may perform one small coherent
  documentation action directly, but not sustained implementation or testing.
- Terra at `medium` is the primary autonomous worker for code, implementation,
  debugging, tests, approved evaluation, and other hands-on engineering.
- Luna at `none` handles substantial deterministic extraction, inventory,
  formatting, reporting, and safe existing-script execution.
- Sol specialist at `high` is optional for an explicitly justified complex or
  high-risk question or independent review.

Delegate only when it separates strategy from execution or costs less than
direct supervisor work. Use one worker for overlapping mutable files or
artifact lineages. Reuse the same worker for rework and closely related work in
the same repository while its context remains useful. Create a new worker for
another repository, independent work, a different role, an unavailable worker,
an explicit independent review, or a deliberate clean-context restart.

## Guaranteed context

Do not assume an agent will discover a useful file. Mandatory information must
be in this file, the selected profile, the supervisor task, or an exact file
that the task explicitly requires the worker to read.

README files, roadmaps, reports, logs, Git history, and `workbench/` are not
automatically read merely because they exist. Before selecting or changing
project work, the supervisor reads the canonical roadmap named in README. A
worker reads only the additional project files required by its task.

## Worker task and autonomy

A substantial task states the goal, relevant current state, mandatory files,
invariants, forbidden actions and human gates, acceptance criteria, and final
report requirements. Describe the result and boundaries; do not predict every
command or file unless it is a real safety or protocol constraint.

Inside those boundaries, the worker owns:

`inspect -> implement -> test -> diagnose -> fix -> retry -> record -> report`

Routine implementation choices, debugging, proportional tests, and correction
of the worker's own changes do not require approval. The worker returns once
with a complete result or one consolidated blocker.

Stop only when the next action requires:

- human approval or a strategic/roadmap decision;
- destructive, external, publishing, privacy-sensitive, or materially
  expensive work not already authorized;
- another repository or material scope expansion;
- credentials, unavailable external information, or resolution of a
  conflicting writer or unrelated user change;
- a decision after repeated diagnostics produce no new evidence.

These are boundary stops, not routine debugging stops.

## Evidence and logs

The worker runs proportional checks and reports the result, changed files,
checks, artifacts or metrics, limitations, and skipped checks.

One `tools/work_log.py` implementation writes two separate journals:

- `reports/agent_tasks.jsonl`: one final worker-attempt record;
- `reports/ml_work.jsonl`: one meaningful ML-work record.

Do not create start or reviewed lifecycle events. Detailed commands, metrics,
hashes, protocols, and artifacts belong in linked reports. If the logging tool
is unavailable or fails, report that with the primary result; do not create a
repair chain unless logging is the assigned task.

`PROJECT_LOG.md` records important accepted milestones and decisions. The
roadmap records current direction and future work. Small safe reports and both
journals are committed; secrets, private data, datasets, model artifacts, and
large generated outputs are not.

## Acceptance and safety

The supervisor reviews the actual result once. Rework normally returns to the
same worker as one consolidated request. Routine work does not require an
independent reviewer or a separate review event.

Never overwrite unrelated user changes or put secrets or private personal
context in repository evidence. Long-running, consequential, destructive, or
externally mutating actions remain human-gated unless the human explicitly
authorized the exact boundary.
