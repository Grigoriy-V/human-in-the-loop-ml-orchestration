# Core Agent Rules

The supervisor defines a bounded task, accepts evidence, and records the final
decision. A worker performs only the approved scope. Each task has one target
repository, one workdir, and one agent ledger.

Use `python tools/agent_ledger.py` for every ledger append; never edit JSONL
history manually. Worker lifecycle events have `supervisor_decision: null`;
only a supervisor appends `reviewed`. Stop on helper, schema, scope, privacy,
or write-conflict failures.

Project adapters add domain-specific rules inside clearly marked adapter
sections. Core templates must not make domain claims. Never sync private
identifiers, secrets, datasets, artifacts, or personal context.
