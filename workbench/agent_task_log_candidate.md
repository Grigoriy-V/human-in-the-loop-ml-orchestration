# Candidate: simplified agent task log

**Status:** discussion candidate only.
**Implementation authorization:** none.

## Problem

The current agent ledger requires a multi-event lifecycle
(`started -> terminal -> reviewed`), a large metadata payload, repeated fields,
and correction events. For small tasks, recording the work can require more
effort than the work itself and can introduce additional failures.

Git alone is not a sufficient replacement: it does not reliably capture failed
or interrupted work, tests and investigations that produced no commit, agent
identity, or the reason a task stopped. Requiring a commit for every agent
action would create a different kind of overhead.

## Candidate goal

Keep a searchable history of agent work while making normal logging a single,
simple action owned by the worker that performed the task.

The log should answer:

- what task was assigned;
- which agent performed it;
- when it finished or stopped;
- whether it completed, failed, or was interrupted;
- what was changed;
- what checks or tests ran and their result;
- what the worker concluded.

It should not require agents to construct JSON, read a schema, repeat task
metadata across lifecycle events, or create a Git commit for every action.

## Normal workflow

1. The supervisor reads the applicable rules and evidence.
2. The supervisor gives one bounded task specification.
3. The worker performs the task and proportional tests or checks.
4. At completion or stop, the worker invokes one logging command.
5. The logging script generates technical metadata and appends one task record.
6. The worker reports the result, changed files, tests, limitations, and the
   generated record ID to the supervisor.
7. The supervisor reviews the actual work and reports the final outcome to the
   user. A separate `reviewed` ledger event is not required.
8. If rework is needed, it is a new bounded worker attempt that may reference
   the earlier task record.

Independent review is not the default. It is reserved for explicitly approved
high-risk, security, privacy, publication, or logging-system changes.

## Proposed worker command

Illustrative interface:

```powershell
python tools/work_log.py agent add `
  --agent terra_worker `
  --task "Update the discussion plan in the roadmap" `
  --status completed `
  --result "Added the agreed discussion-only section." `
  --tests "git diff --check: passed"
```

For a stopped task:

```powershell
python tools/work_log.py agent add `
  --agent terra_worker `
  --task "Update the discussion plan in the roadmap" `
  --status failed `
  --result "Stopped before editing because the target file had an unexpected change." `
  --tests "not run: stopped during preflight"
```

The command names and arguments are provisional. The important constraint is
one normal worker call per task outcome.

## Worker-supplied information

Keep manually supplied information small:

- agent or profile;
- short task description;
- outcome status: `completed`, `failed`, or `interrupted`;
- concise result or stop reason;
- tests/checks and their result, including an explicit reason when none ran.

Token and cost data are outside this log. If Codex later exposes useful native
usage reporting, it may be analyzed separately without changing the task-log
workflow. Agents must not estimate, reconstruct, or manually record usage.

## Script-generated information

The script should generate or inspect everything reasonably available:

- unique record ID;
- system UTC timestamp;
- repository identity and working directory;
- current branch and HEAD;
- changed and untracked repository-relative files;
- log format and schema version;
- safe append/locking details.

The script should reject unsafe paths and secret-like values, but error
messages must name the exact invalid or missing input. Internal schema and
locking mechanics must not be part of the normal agent instructions.

## Storage and retrieval

The provisional storage is one append-only record per worker attempt, for
example `reports/agent_tasks.jsonl`. JSONL remains an implementation detail;
agents and humans use the script.

The same tool should support:

```powershell
python tools/work_log.py agent list
python tools/work_log.py agent list --status failed
python tools/work_log.py agent search "roadmap"
python tools/work_log.py agent search --file PROJECT_ROADMAP.md
python tools/work_log.py agent show <record-id>
```

This provides task history without requiring a Git commit for every action.
Git remains the source of truth for committed file history and code diffs.

## Relationship to incident learning

The task log records ordinary agent work. A separate
`ORCHESTRATION_INCIDENTS.md` candidate would record only important failures,
repeated waste, rule conflicts, and lessons that may change the system.

An incident may reference one or more task record IDs. Routine task records do
not automatically become incidents.

## Minimal agent instruction

The complete normal-use rule should fit directly in `AGENTS.md`:

> The supervisor defines a bounded task and reviews the result. The worker
> performs the task and proportional tests. On completion or stop, the worker
> runs `python tools/work_log.py agent add` once with agent, task, status, result,
> and tests. The script adds time, ID, Git state, changed files, and repository
> metadata. The worker returns the record ID and evidence to the
> supervisor. Separate start and review events are not required.

`python tools/work_log.py agent --help` should contain one short working
example.
No other documentation should be required for normal logging.

## Simplicity constraints

- One normal record per worker attempt.
- No mandatory `started` event.
- No separate supervisor `reviewed` event.
- No hand-written JSON or metadata payload.
- No schema reading during normal work.
- No mandatory commit.
- No independent reviewer for routine tasks.
- No token or cost fields and no custom usage collector.
- Do not add a field unless it supports a concrete audit or improvement query.

## Relationship to project adapters

The task-log format is universal. Project adapters may define how work is
performed, stopped, tested, and reported, but they do not add project-specific
fields to this log. Domain details belong in linked reports or in the concise
result text.

## Questions to resolve before implementation

1. Whether the worker-supplied `agent` value can be detected reliably.
2. Whether exact executed commands are needed in the task log or a concise
   tests/checks summary is sufficient.
3. Whether hard-crash tasks with no final worker call need a lightweight
   supervisor recovery record.
4. The minimum search and reporting queries needed for the first iteration.
5. Whether task records are committed to Git or retained as local operational
   evidence and summarized periodically.

No implementation should begin until these questions and the candidate's
purpose are discussed and accepted.
