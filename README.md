# Human-in-the-Loop ML Orchestration

This repository is a compact development hub for a human-supervisor-worker
agent system. It exists to improve agent instructions, delegation, context
handling, evidence, and operating cost through real experience in connected ML
projects.

Core does not control or automatically synchronize those projects. It stores a
universal project foundation, develops small supporting tools, audits
explicitly connected repositories, and preserves reusable lessons.

## Current state

The minimal instruction foundation is accepted. The previous v0.2
implementation, templates, adapters, tools, tests, documentation, and evidence
are isolated under `old/v0_2/` and are not active.

`work_log.py` has not been implemented. Bootstrap and adapter work are
deferred.

## Entry points

- `AGENTS.md`: automatically loaded universal operating contract.
- `PROJECT_ROADMAP.md`: current Core direction and approved step.
- `PROJECT_LOG.md`: important completed milestones and decisions.
- `docs/`: project documentation; intentionally empty for now.
- `tools/`: shared project tools; intentionally empty until `work_log.py` is
  implemented.
- `tests/`: tests for active project tools and rules; intentionally empty for
  now.
- `reports/agent_tasks.jsonl`: final worker outcomes; empty until the tool
  exists.
- `reports/ml_work.jsonl`: meaningful ML work; empty until the tool exists.
- `workbench/`: discussion candidates, incidents, audits, and design evidence.
- `old/v0_2/`: inactive historical implementation and evidence.

The connected repositories are:

- `D:\ML\My_first_model`: generative ML reference;
- `D:\ML\product-conversion-ml-case`: classical ML case.

They are read-only from Core unless the human separately authorizes work inside
the target repository.

## Intended project foundation

```text
new-project/
|-- README.md
|-- AGENTS.md
|-- PROJECT_ROADMAP.md
|-- PROJECT_LOG.md
|-- .codex/
|   |-- config.toml
|   `-- agents/
|       |-- terra_worker.toml
|       |-- luna_clerk.toml
|       `-- sol_specialist.toml
|-- docs/
|-- tools/
|   `-- work_log.py        # not implemented yet
|-- tests/
`-- reports/
    |-- agent_tasks.jsonl
    `-- ml_work.jsonl
```

README is the first manual adaptation surface for a project. Domain rules,
reports, and documentation are added only when the project needs them.

## Operating boundary

Discussion and roadmap updates do not authorize implementation. Work starts
from the current approved roadmap step only after an explicit human command.
Long-running, consequential, destructive, or externally mutating actions
remain human-gated.
