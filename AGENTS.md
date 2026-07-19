# Core Agent Rules

The root/main agent is supervisor-only: it reads local evidence and Git state,
defines bounded work, reviews evidence, and records the final decision. Every
worker task specifies its scope, one target repository/workdir/agent ledger,
allowed files or artifacts, allowed commands or milestones, stop conditions,
reporting requirements, and acceptance criteria. Workers perform only the
approved implementation, inspection, tests, and other commands.

Use `luna_clerk` with reasoning `none` only for deterministic clerical work,
`terra_worker` at `low` for normal bounded implementation/validation, and
`sol_specialist` at `high` only after explicit supervisor approval for complex
or high-risk work. Workers do not change model, reasoning, scope, or delegate
without approval.

Use one write-heavy worker for overlapping mutable paths or artifacts. Use
`python tools/agent_ledger.py` for every ledger append; never edit JSONL
history manually. Every worker task appends `started` and exactly one terminal
event; only a supervisor appends `reviewed`. Worker lifecycle events have
`supervisor_decision: null`. Stop on helper, schema, scope, privacy, or
write-conflict failures and report exact commands, changed files, results,
stop conditions, uncertainty, and all appended event IDs.

Project adapters add domain-specific rules inside clearly marked adapter
sections. Core templates must not make domain claims. Never sync private
identifiers, secrets, datasets, artifacts, or personal context.

Long-running, consequential, destructive, or externally mutating commands are
human-gated. Domain overlays may add stricter gates and may not weaken this
boundary.
