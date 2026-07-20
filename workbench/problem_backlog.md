# Orchestration problem backlog

**Status:** discussion backlog. No implementation is authorized by this file.

## 1. Agent and ML work logs and incidents

**Discussion status:** discussed; simplified candidates prepared, implementation
not started.

- Replace the current complex multi-event lifecycle with a simple worker-owned
  final task record.
- Generate technical fields through a script rather than by the agent.
- Keep the agent log universal: task, agent, outcome, concise result, checks,
  and automatically generated repository metadata.
- Keep the ML work log universal: short summary, result or stop reason,
  decision or limitation, and links to detailed reports or artifacts.
- Keep project-specific metrics, checkpoints, configurations, and other domain
  details in linked reports rather than adding adapter-specific log fields.
- Keep normal task history searchable without requiring a Git commit for every
  action.
- Keep important orchestration incidents as simple workbench notes rather than
  mixing them with routine task logs.

Related candidates:

- `workbench/agent_task_log_candidate.md`;
- `workbench/ml_work_log_candidate.md`;
- `workbench/project_log_file_candidate.md`.

## 2. Supervisor, delegation, and worker autonomy

**Discussion status:** discussed at candidate level; the boundaries still need
validation through real tasks.

- The human acts as client and controls the transition from discussion to work.
- Sol supervises strategy, task design, routing, and acceptance.
- Terra autonomously owns implementation, testing, evaluation, debugging, and
  retry inside the approved result and boundaries.
- Luna handles substantial deterministic clerical work when delegation is
  cheaper than direct Sol action.
- Avoid micro-tasks, routine approval loops, and repeated supervisor/worker
  handoffs.
- Define the boundary for small direct Sol actions, worker retry limits,
  evaluation gates, and minimum acceptance evidence.

Related candidate: `workbench/orchestration_roles_candidate.md`.

## 3. Instructions and context management

**Discussion status:** discussed; combined system draft prepared, implementation
not started.

- Deliver every mandatory instruction through an automatic source such as
  `AGENTS.md`, an active profile/config, or an explicit required-read item in
  the supervisor task.
- Keep `AGENTS.md` short and complete for universal rules; use profiles for role
  specialization and the task specification for task-specific context.
- Reuse a worker for related work in the same repository and task lineage;
  create a new worker for independent work, another repository or role, or a
  deliberate clean context.
- Configure automatic compaction through the runtime rather than asking an
  agent to estimate context usage. The provisional Terra threshold is 165000
  tokens and Terra reasoning is `medium`.
- Keep decisions and current state in repository files; context summaries are
  not the sole source of truth.

Related draft: `workbench/orchestration_system_draft.md`.

## 4. Resource usage and optimization

**Discussion status:** discussed and deferred.

- Do not build a custom token or cost accounting system.
- Use native Codex usage data only if the active runtime exposes it
  automatically and without changing the worker workflow.
- Do not add token or cost fields to the agent or ML work logs.
- For the current desktop worker flow, use the existing usage view only as an
  occasional diagnostic signal.
- Revisit automated usage analysis only if a painless native interface becomes
  available.

## 5. Roadmap operating rules

**Discussion status:** discussed; self-documenting roadmap candidate prepared,
implementation not started.

- Define how agents read and use the canonical roadmap.
- Add concise evidence or logs for completed roadmap stages.
- Move through the roadmap one approved step at a time.
- Discuss and accept the next step before expanding work.
- Keep completed evidence, current state, and future ideas distinguishable.
- Prevent agents from silently skipping, combining, or inventing roadmap
  stages.

The candidate must be explicitly accepted before changing the active roadmap
policy.

Related candidate: `workbench/roadmap_file_candidate.md`.

## 6. Orchestration file inventory and project summaries

**Discussion status:** scope and foundation candidate prepared; a read-only
audit of both ML repositories is the required next step before implementation.

Create a clear inventory of files used to build a new project foundation or
inspect agent orchestration across existing repositories.

The inventory should cover:

- agent rules and profiles;
- orchestration documentation;
- task and logging tools;
- schemas and validation rules;
- roadmap and relevant operational evidence;
- project-specific orchestration additions;
- files that are copied only during initial bootstrap;
- files that remain project-owned after creation;
- files that Core reads during an approved audit.

The inventory must preserve project uniqueness rather than treating every
difference as drift.

Also create a short summary for each connected project or adapter, including:

- why the repository exists;
- its primary task and current role;
- what makes it different from the other projects;
- which orchestration rules are universal;
- which rules, tools, evidence, and gates are domain-specific;
- which files Core reads during an audit;
- what must remain project-owned and must not be overwritten.

Initial summaries are needed for:

- the orchestration Core;
- the generative-ML repository;
- the classical-ML repository.

Bootstrap creates one universal foundation without selecting an adapter.
`README.md` is the first manual adaptation surface, and the base includes
`PROJECT_LOG.md`, an initially empty `docs/` directory, and stable universal
`agent_log.py` and `ml_log.py` tools.

Automatic tracking and synchronization are deferred. Start later with one
simple read-only difference script over an explicit file list.

Related candidates:

- `workbench/repository_foundation_candidate.md`;
- `workbench/ml_repositories_audit_plan.md`.
