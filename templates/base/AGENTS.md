# Project Agent Rules

The root/main agent is supervisor-only. It reads the roadmap, reports, ledgers,
and Git state; defines a bounded task with scope, allowed files, commands or
milestones, stop conditions, reporting requirements, and acceptance criteria;
then reviews evidence and makes the final decision.

Workers perform code inspection, implementation, routine investigation, tests,
and other approved commands. Use `luna_clerk` with reasoning `none` only for
deterministic clerical work, `terra_worker` at `low` for default bounded work,
and `sol_specialist` at `high` only after explicit supervisor approval for
complex or high-risk work. Workers must not change model, reasoning, scope, or
delegate without approval.

Every repository task appends lifecycle events only through
`python tools/agent_ledger.py`. Use a metadata file for PowerShell starts.
Each worker appends `started` and exactly one terminal event. Worker `started`,
`completed`, `failed`, and `interrupted` events have `supervisor_decision:
null`; only the supervisor appends `reviewed`. Report exact commands, changed
files, results, stop conditions, uncertainty, and all appended event IDs.

One task has one repository, workdir, and ledger. Stop on helper/schema failure,
write conflict, scope ambiguity, privacy risk, or a human gate. Long-running,
consequential, destructive, or externally mutating commands require explicit
human approval. Never put secrets, private context, large artifacts, or
machine-specific absolute paths in reusable project files.

Adapter-owned rules extend these generic rules and must not weaken them.
