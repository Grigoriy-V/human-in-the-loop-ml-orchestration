# Draft: orchestration instructions, profiles, and context inventory

**Status:** workbench draft only.
**Implementation authorization:** none.
**Target:** a future simplified orchestration system derived from the accepted
discussion candidates.

This file intentionally keeps the proposed contents of several future files in
one place. The sections may later be split into active files only after review.

**Later scope correction:** sections that assume adapter overlays, ongoing
Core ownership, managed-file synchronization, or the earlier scaffold
inventory are superseded by
`workbench/repository_foundation_candidate.md`. The current direction is one
universal bootstrap foundation, manual project adaptation, and read-only audit
of existing repositories.

Related discussion candidates:

- `workbench/orchestration_roles_candidate.md`
- `workbench/agent_task_log_candidate.md`
- `workbench/ml_work_log_candidate.md`
- `workbench/project_log_file_candidate.md`
- `workbench/roadmap_file_candidate.md`
- `workbench/repository_foundation_candidate.md`
- `workbench/ml_repositories_audit_plan.md`
- `workbench/problem_backlog.md`

## 1. Context delivery invariant

The system must not rely on an agent independently discovering a useful file.

Information is mandatory only when it reaches the agent through one of these
guaranteed routes:

1. **Automatic durable context**
   - the applicable `AGENTS.md`;
   - the selected custom-agent profile;
   - behavior applied by `.codex/config.toml`.
2. **Explicit task context**
   - the information is included directly in the supervisor task;
   - or the task explicitly requires the agent to read a named file before
     implementation.

A file is not considered read merely because it exists, is linked from another
document, has a familiar name, or appears useful.

README files, roadmaps, reports, ledgers, workbench notes, Git history, and
architecture documents are not automatic context unless an applicable
`AGENTS.md` or the current task explicitly requires them.

If a file contains a constraint that is essential to safe implementation, one
of the following must be true:

- the essential constraint is stated directly in `AGENTS.md`;
- `AGENTS.md` explicitly requires that file for the applicable category of
  work;
- the supervisor explicitly names the file in the worker task and states why
  it is mandatory.

## 2. Context layers

### Layer A: automatic operating contract

The applicable `AGENTS.md` contains the complete short operating contract:

- human, supervisor, Terra, and Luna roles;
- discussion versus execution;
- routing;
- worker autonomy;
- human gates;
- task completion and acceptance;
- roadmap transition rules;
- guaranteed-context rules.

Critical behavior must not depend on following a chain of documentation links.

### Layer B: active agent specialization

The selected profile contains only role-specific behavior:

- model and reasoning;
- role boundary;
- autonomy appropriate to the role;
- compaction settings where needed.

Common orchestration rules are not duplicated across every profile.

### Layer C: task-specific context

The supervisor task provides:

- goal;
- current state relevant to the goal;
- mandatory files to read;
- invariants and protocol;
- forbidden actions and human gates;
- acceptance criteria;
- expected final report.

The worker does not read the whole project archive unless the task is an audit
that explicitly requires it.

### Layer D: project source of truth

Project state survives thread loss or context compaction through repository
files:

- canonical roadmap;
- project orchestration profile/summary;
- code and configuration;
- accepted reports and results;
- task log;
- domain-specific evidence when applicable.

Agent-thread history and compacted summaries are never the sole source of
truth.

### Layer E: history and design material

Historical reports, task logs, incidents, Git history, and `workbench/` are
read only when the task requires audit, recovery, system design, or a known
repeated problem.

They are not normal runtime context.

## 3. Proposed future `AGENTS.md`

The following is candidate content, not an active policy.

```markdown
# Agent operating contract

## Human and execution gate

The human is the client and learning partner. Discussion is the default mode.
Discussion, questions, ideas, and candidates do not authorize implementation.

Commands such as "start work", "continue work", or "follow the plan" move the
agreed direction into execution. The supervisor then formulates and dispatches
the next bounded task within existing human gates. The human is not required to
write a technical specification, select an agent, or transfer instructions
between chats.

## Supervisor

The main Sol agent is the supervisor. It owns interpretation, strategy,
roadmap use, task design, routing, coordination, acceptance, and the final
report to the human.

The supervisor reads project evidence and may perform one small coherent
documentation or roadmap action directly when delegation would cost more than
the action. It does not perform sustained implementation, test, benchmark,
evaluation, or training work.

The supervisor is accountable for unclear tasks, wrong routing, unnecessary
handoffs, omitted boundaries, and inadequate acceptance review.

## Routing

- Sol supervisor: discussion, strategy, task design, small direct
  documentation actions, and acceptance.
- Terra worker: code, implementation, debugging, tests, benchmarks,
  evaluations, and other hands-on engineering.
- Luna clerk: substantial deterministic extraction, inventory, formatting,
  reporting, and execution of existing safe scripts when delegation is cheaper
  than direct Sol work.
- Sol specialist: optional independent complex or high-risk review only when
  explicitly justified.

Do not delegate a trivial action when the task specification, lifecycle, and
handoff would cost more than direct completion.

## Guaranteed context

Do not assume an agent will discover a useful file.

Mandatory information must be present in this `AGENTS.md`, in the selected
agent profile, directly in the supervisor task, or in a file that the
supervisor task explicitly requires the worker to read.

Before selecting a new project step, the supervisor reads the canonical
roadmap and the project orchestration profile. The worker reads only the
roadmap step, reports, protocols, or other files explicitly named in its task.

## Worker task

A substantial worker task defines:

1. goal;
2. relevant current state and mandatory files;
3. invariants or protocol;
4. forbidden actions and human gates;
5. acceptance criteria;
6. final report requirements.

Describe the result and boundaries. Do not enumerate every permitted command
or predict every file unless those details are genuine safety or protocol
requirements.

## Terra autonomy

Terra owns the complete execution loop inside the assigned result and
boundaries:

inspect -> implement -> test -> diagnose -> fix -> retry -> record -> report.

Routine implementation decisions, local debugging, correction of the worker's
own changes, and retries inside the approved cost/protocol boundary do not
require new supervisor approval.

Terra returns only when the result is complete or when a real boundary blocks
progress. A blocker report consolidates what was attempted, the exact blocker,
what was ruled out, the recommended next decision, and the authority or
information required.

Logging failure does not invalidate completed primary work. Report it with the
normal result instead of starting a separate repair chain unless logging is
the assigned task.

## Stop and human gates

Stop and return control when the next action requires:

- human approval;
- destructive, externally mutating, publishing, or materially expensive work
  not already authorized;
- a strategic or roadmap change;
- material scope expansion or another repository;
- credentials, secrets, or unavailable external information;
- resolution of a conflicting writer or unrelated user change;
- a decision after repeated diagnostics produce no new evidence.

These are boundary stops, not routine debugging stops.

## Worker reuse

Reuse the existing primary worker for continuing work in the same repository
and supervisor thread. Rework and closely related next steps go to the same
worker whenever it remains available and its context is useful.

Create a new worker for a different repository, independent parallel work,
fresh independent review, an unavailable worker thread, a different role, or
an explicit need for clean context.

A worker thread is not a permanent project database. A new supervisor chat
creates a new worker and restores state from repository sources of truth.

## Completion and acceptance

The worker runs proportional checks and returns:

- result;
- changed files;
- tests/checks and outcomes;
- relevant artifacts or metrics;
- limitations and skipped checks;
- one simplified task-log record ID, or the logging error.

The supervisor reviews the actual result once. If rework is needed, send the
same worker one consolidated set of findings. Routine work does not require a
separate independent reviewer or a separate reviewed ledger event.

## Roadmap

Use one canonical roadmap. The supervisor reads it before selecting the next
step.

Work on one approved roadmap step at a time. Do not silently skip, merge,
invent, or expand steps. Record concise evidence for a completed step, accept
or rework it, and discuss the next transition before starting it.

Keep completed evidence, current state, and future ideas distinguishable.
```

## 4. Proposed future `.codex/config.toml`

Candidate only. Model identifiers and supported values must be verified in the
active Codex environment before implementation.

```toml
# Main project conversation: Sol supervisor.
model = "gpt-5.6-sol"
model_reasoning_effort = "high"

[agents]
# Keep coordination bounded. Policy still allows only one overlapping writer.
max_threads = 2
max_depth = 1
```

Notes:

- `max_depth = 1` prevents workers from delegating further.
- `max_threads` is a cap, not permission to create parallel writers.
- The normal pattern is one main Sol plus one active Terra or Luna task.
- Compaction is configured in the long-lived Terra profile rather than imposed
  on every short session.

## 5. Proposed future `.codex/agents/terra_worker.toml`

The human requested Terra at `medium` reasoning.

The assumed context window is approximately `258K` tokens and must be verified.
The provisional automatic compaction threshold is `165000` tokens, slightly
below 65% of 258K.

```toml
name = "terra_worker"
description = "Primary autonomous hands-on worker for implementation, tests, debugging, evaluation, and related engineering."
model = "gpt-5.6-terra"
model_reasoning_effort = "medium"

# Provisional: 258K context window must be verified.
model_auto_compact_token_limit = 165000
model_auto_compact_token_limit_scope = "total"

compact_prompt = """
Preserve the active task goal, mandatory files, invariants, forbidden actions,
human gates, acceptance criteria, decisions already made, changed files,
commands and tests already run, verified results, current blockers, remaining
work, and repository paths that are sources of truth. Remove verbose tool
output, repeated discussion, superseded hypotheses, and resolved diagnostics.
Do not invent completion or results.
"""

developer_instructions = """
Follow the applicable AGENTS.md and the supervisor task.

Own the complete execution loop inside the assigned result and boundaries:
inspect, implement, test, diagnose, fix, retry, record, and report.

Use judgment for implementation details and necessary in-scope files and
commands. Do not request routine approval for debugging, tests, or correction
of your own work. Do not change project strategy, roadmap direction, human
gates, repository scope, model, reasoning, or delegation depth.

Return one complete result or one consolidated blocker report.
"""
```

The runtime, not the model, should trigger compaction. Terra must not estimate
its own context percentage.

## 6. Proposed future `.codex/agents/luna_clerk.toml`

```toml
name = "luna_clerk"
description = "Autonomous clerk for substantial deterministic extraction, inventory, formatting, reporting, and safe existing-script execution."
model = "gpt-5.6-luna"
model_reasoning_effort = "none"

developer_instructions = """
Follow the applicable AGENTS.md and the supervisor task.

Complete bounded deterministic clerical work autonomously and return one
result. Do not make strategy or project decisions, implement or debug code,
design experiments, interpret ambiguous results, change model or reasoning, or
delegate.

Do not accept a trivial one-line action when delegation overhead would exceed
direct supervisor work; report the mismatch without starting a work chain.
"""
```

Luna is expected to handle shorter tasks, so a profile-specific compaction
threshold is not proposed initially.

## 7. Proposed future `.codex/agents/sol_specialist.toml`

This is not the main supervisor. It is an optional spawned specialist.

```toml
name = "sol_specialist"
description = "Optional independent specialist for explicitly justified complex or high-risk analysis and review."
model = "gpt-5.6-sol"
model_reasoning_effort = "medium"

developer_instructions = """
Follow the applicable AGENTS.md and the explicit specialist task.

Work only on the approved complex or high-risk question. Return findings,
evidence, uncertainty, and a recommendation. Do not replace the main
supervisor, broaden project direction, perform routine implementation, or
delegate.
"""
```

Candidate use cases:

- security or privacy review;
- publication or externally visible release;
- destructive or high-risk migration;
- changes to logging, validation, or governance;
- a complex blocker that Terra cannot resolve.

Routine work does not use this profile.

## 8. Proposed context-compaction policy

### Assumption

- Terra context window: approximately `258K` tokens.
- This value is unverified and may differ by model/runtime.
- Initial threshold candidate: `165000` total tokens.

### Behavior

- Codex runtime triggers automatic compaction at the configured token limit.
- The agent does not estimate context percentage.
- The same Terra thread continues after compaction.
- The compact prompt preserves the active execution state and references to
  repository sources of truth.
- The next supervisor task still provides its own goal and mandatory context.

### Safety

Compaction must not be the sole persistence mechanism for:

- accepted decisions;
- roadmap state;
- experiment results;
- exact commands and hashes required as evidence;
- unresolved human gates;
- task completion records.

Those facts remain in repository files.

### Review after initial use

When resource tracking becomes available, evaluate:

- compaction frequency;
- tokens spent on compaction;
- whether tasks lose necessary state after compaction;
- whether `165000` is too early or too late;
- whether `total` or `body_after_prefix` is the better scope.

## 9. Proposed worker creation and reuse policy

### Reuse an existing worker when

- the same task continues;
- supervisor review requests rework;
- the next task is closely related and in the same repository;
- the same code/output/experiment lineage remains owned;
- the agent thread is available;
- existing context is useful and not misleading.

The supervisor sends a follow-up to the existing worker thread rather than
spawning another worker with the same profile.

### Create a new worker when

- work targets another repository;
- a task is independent and may run in parallel safely;
- a fresh independent review is explicitly required;
- the prior thread is unavailable or closed;
- a different role or model is needed;
- the prior context is materially misleading and a repository-based clean
  reconstruction is safer.

### Thread lifetime boundary

The "primary Terra" is persistent within the current supervisor thread, not
necessarily across all Codex chats.

When a new supervisor chat begins:

1. load the applicable automatic instructions;
2. read the project orchestration profile and canonical roadmap;
3. reconstruct current state from accepted repository evidence;
4. spawn a new primary Terra when execution is authorized;
5. pass the task-specific context explicitly.

## 10. Proposed future orchestration file inventory

The inventory distinguishes instruction delivery, operational purpose,
ownership, and synchronization behavior.

### Delivery classes

- `automatic_instruction`: loaded into model context automatically.
- `automatic_config`: behavior is applied by Codex configuration.
- `explicit_required`: must be named by `AGENTS.md` or the current task.
- `conditional_evidence`: read only for a relevant task or audit.
- `history_only`: not normal runtime context.
- `never_runtime_context`: must not be loaded into agent context.

### Ownership/sync classes

- `core_shared`: generic policy intended to remain common.
- `project_override`: project version may intentionally differ.
- `project_owned`: Core must not overwrite it.
- `mutable_evidence`: operational history, not managed policy.
- `private_never_sync`: must not enter repository sync or public evidence.

### Current and proposed files

| File or pattern | Purpose | Delivery | Ownership/sync |
| --- | --- | --- | --- |
| `AGENTS.md` | Complete short operating contract | `automatic_instruction` | `core_shared` plus clearly marked project additions |
| Nested `AGENTS.md` | Subtree-specific rules when present | `automatic_instruction` | `project_override` |
| `.codex/config.toml` | Main model and agent runtime configuration | `automatic_config` | `core_shared` with project override |
| `.codex/agents/terra_worker.toml` | Terra specialization and compaction | `automatic_instruction` when Terra is spawned | `core_shared` with project override |
| `.codex/agents/luna_clerk.toml` | Luna specialization | `automatic_instruction` when Luna is spawned | `core_shared` with project override |
| `.codex/agents/sol_specialist.toml` | Optional specialist specialization | `automatic_instruction` when explicitly spawned | `core_shared` with project override |
| Canonical roadmap | Current accepted direction and next step | `explicit_required` for supervisor step selection | `project_owned` |
| `orchestration/project_profile.md` (proposed) | Repository purpose, role, uniqueness, domain gates, and context entrypoints | `explicit_required` for supervisor state reconstruction | `project_owned` |
| `orchestration/orchestration_files.json` (proposed) | Machine-readable orchestration inventory and sync classification | `conditional_evidence` | `project_owned` derived from Core categories |
| `docs/agent_orchestration.md` | Extended background or examples only | `conditional_evidence` | `core_shared` or removable if redundant |
| `docs/lifecycle.md` | Legacy/current lifecycle explanation | `history_only` after simplified logging replaces it | `core_shared` until migration |
| `reports/agent_tasks.jsonl` (proposed) | One final record per worker attempt | `conditional_evidence` | `mutable_evidence` |
| Current `reports/agent_execution_ledger.jsonl` | Historical multi-event worker evidence | `history_only` after migration | `mutable_evidence` |
| Experiment ledger | Domain ML evidence | `explicit_required` only for relevant ML tasks and audits | `project_owned` |
| `PROJECT_LOG.md` | Accepted project milestones and evidence pointers | `conditional_evidence` | `mutable_evidence` |
| Accepted technical reports | Task/experiment evidence | `explicit_required` when relevant to the current task | `project_owned` |
| `workbench/problem_backlog.md` | Orchestration discussion backlog | `history_only` except system-design work | `project_owned` |
| `workbench/*_candidate.md` | Unaccepted design candidates | `history_only` except system-design work | `project_owned` |
| `workbench/incidents.md` (proposed) | Simple important orchestration incidents and lessons | `conditional_evidence` for orchestration improvement | `project_owned` |
| `orchestration.lock.json` | Core provenance and managed-file relationships | `conditional_evidence` for sync/audit | `project_owned` |
| Core manifests/schemas | Machine verification of declared managed files | `conditional_evidence` for sync/audit | `core_shared` |
| Secrets, credentials, private identity, private personal context | Forbidden context and sync material | `never_runtime_context` | `private_never_sync` |

## 11. Proposed future `orchestration/project_profile.md`

Each connected repository should have a short self-contained profile.

```markdown
# Project orchestration profile

## Purpose

Why this repository exists.

## Current role

What the project currently contributes to the wider workspace.

## Primary work

The kinds of tasks and outcomes performed here.

## Unique characteristics

What distinguishes this repository from Core and other projects.

## Canonical state

- canonical roadmap:
- current status:
- primary evidence:

## Universal orchestration rules

Which Core rules apply unchanged.

## Project-specific rules and gates

Domain rules, evidence requirements, human gates, artifacts, and safety
boundaries that must remain local.

## Required context entrypoints

Files the supervisor must read when reconstructing this project's state.

## Sync boundary

- may be synchronized from Core:
- intentionally adapted:
- project-owned:
- never synchronize:
```

Initial profiles:

- orchestration Core;
- generative-ML repository;
- classical-ML repository.

## 12. Proposed future machine-readable orchestration inventory

The human-readable table in this draft can later become a small manifest such
as `orchestration/orchestration_files.json`.

Minimum record:

```json
{
  "path": "AGENTS.md",
  "purpose": "automatic operating contract",
  "delivery": "automatic_instruction",
  "ownership": "core_shared",
  "sync": "managed",
  "required_for": ["all_agents"]
}
```

The manifest is for synchronization and audit. It must not become another
large instruction file agents are expected to read during normal work.

## 13. Draft simplification rules

1. Critical behavior lives in the automatically loaded `AGENTS.md`.
2. Profiles contain specialization, not copies of the complete common policy.
3. Task-specific mandatory files are named directly in the supervisor task.
4. The project profile and roadmap are supervisor context, not mandatory
   reading for every worker.
5. Workbench and historical evidence are opt-in context.
6. Automatic compaction is a runtime setting, not a model judgment.
7. Agent threads are reusable execution context, not project databases.
8. New files are added to the context inventory only when they have a concrete
   orchestration or audit role.
9. A file that is important but has no guaranteed delivery path is a design
   defect.
10. Instruction and logging mechanisms must remain cheaper than the work they
    coordinate.

## 14. Items requiring verification before activation

- Confirm the actual Terra context window; `258K` is currently an assumption.
- Confirm `model_auto_compact_token_limit` works in the project-scoped Terra
  profile in the active Codex app/runtime.
- Confirm `gpt-5.6-sol`, `gpt-5.6-terra`, and `gpt-5.6-luna` identifiers and
  supported reasoning values in the target environment.
- Decide whether the main model belongs in project `.codex/config.toml` or is
  selected by the human/session.
- Decide whether `max_threads = 2` matches the intended one-worker workflow in
  the active app.
- Define the first minimal simplified task-log schema and command.
- Define the minimal roadmap stage evidence.
- Decide whether extended orchestration docs are retained as background or
  removed after `AGENTS.md` becomes self-contained.
- Validate that future Core sync preserves project-owned profiles, roadmaps,
  evidence, and domain-specific rules.

No active orchestration file should be changed until this draft is reviewed
and the applicable sections are accepted.
