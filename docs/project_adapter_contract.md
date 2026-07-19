# Project adapter contract

An adapter is self-contained: its own `AGENTS.md`, `.codex`, helpers, schemas,
ledgers, roadmap, log, Core pin, and managed-file declaration.

In v0.2 bootstrap, the entire immutable target-file inventory is declared in
`core/managed_files.json` and pinned in `orchestration.lock.json`. Generic
files come from `templates/base`; adapter additions or replacements come from
one explicit declared overlay. `base_copy` and `overlay_copy` are byte-identical
relationships whose target and Core source hashes must match.

Mutable roadmaps, logs, reports, and JSONL ledgers are target-owned and never
appear in the managed inventory. Domain overlays may add policy but may not
weaken supervisor-only control, lifecycle evidence, privacy, or human gates.

This candidate does not implement sync application. Future propagation must
detect versions and conflicts, preserve adapter-owned mutable content, and
remain human-reviewed before `--apply` can be enabled.
