# Project Log

This file records important completed milestones and decisions. Add one dated
entry after a material result, not after every task or test. Keep Outcome and
Decision short and link to detailed evidence when needed.

## 2026-07-20: Orchestration redesign and repository audit

### Outcome

The human-supervisor-worker model, guaranteed context rules, simplified logs,
roadmap, PROJECT_LOG, and minimal repository foundation were discussed. The
generative and classical ML repositories were audited read-only; detailed
evidence is in `workbench/ml_repositories_orchestration_audit.md`.

### Decision

Use Sol as supervisor, Terra at `medium` for autonomous engineering, and Luna
only for substantial deterministic work. Use one future `work_log.py` with
separate agent and ML journals. Do not build token accounting, automatic sync,
or domain-specific log schemas.

## 2026-07-20: Clean Core foundation candidate

### Outcome

Created the new active `AGENTS.md`, config, agent profiles, README, roadmap,
and project log. Moved the v0.2 implementation, templates, adapters, tools,
tests, schemas, manifests, reports, and documentation to `old/v0_2/`.

The active root now contains the foundation candidate, empty tracked `docs/`,
`tools/`, and `tests/` directories, two empty work journals, and the Core
workbench. The active rules were corrected to make repository scope, supervisor
accountability, roadmap discipline, and the inactive logging state explicit.

### Decision

Treat `old/v0_2/` as historical reference, not active instructions or
implementation. Explicitly accept the foundation before selecting the next
development step. Bootstrap and adapter work remain deferred.

## 2026-07-20: Minimal foundation accepted

### Outcome

A fresh Terra worker received only the automatic `AGENTS.md` contract and its
selected profile. It correctly reported Terra `medium`, the human and
supervisor boundaries, the autonomous execution loop, real stop conditions,
non-automatic context sources, and inactive logging. It returned once without
editing files, running tests, invoking logging, delegating, or requesting
routine approval.

The active configuration uses Sol supervisor `medium`, Terra `medium`, Luna
`none`, and optional Sol specialist `medium`.

### Decision

Accept the minimal foundation as the active Core baseline. Keep
`tools/work_log.py` as the next candidate; its implementation remains a
separate step.
