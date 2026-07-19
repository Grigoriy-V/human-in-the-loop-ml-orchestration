# Core Agent Rules

The root/main agent is supervisor-only: it defines bounded work, reviews
evidence, and records the final decision. Workers perform implementation,
inspection, tests, and other approved commands. Each task has one target
repository, one workdir, and one agent ledger.

Use `luna_clerk` with reasoning `none` only for deterministic clerical work,
`terra_worker` at `low` for normal bounded implementation/validation, and
`sol_specialist` at `high` only after explicit supervisor approval for complex
or high-risk work. Workers do not change model, reasoning, scope, or delegate
without approval.

Use `python tools/agent_ledger.py` for every ledger append; never edit JSONL
history manually. Worker lifecycle events have `supervisor_decision: null`;
only a supervisor appends `reviewed`. Stop on helper, schema, scope, privacy,
or write-conflict failures.

Project adapters add domain-specific rules inside clearly marked adapter
sections. Core templates must not make domain claims. Never sync private
identifiers, secrets, datasets, artifacts, or personal context.

Long-running, consequential, destructive, or externally mutating commands are
human-gated. Domain overlays may add stricter gates and may not weaken this
boundary.
