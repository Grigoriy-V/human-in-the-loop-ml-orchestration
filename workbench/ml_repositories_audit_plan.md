# Plan: pre-implementation ML repository audit

**Status:** completed on 2026-07-20.
**Implementation authorization:** none.

**Result:** see `workbench/ml_repositories_orchestration_audit.md`.

## Purpose

Audit real human-agent work before implementing the new Core foundation. The
audit must test whether the current candidates solve observed problems without
discarding information that was actually useful.

The audit is about orchestration, not ML model quality.

## Repositories

- Generative ML: `D:\ML\My_first_model`
- Classical ML: `D:\ML\product-conversion-ml-case`

## Safety and scope

The audit is read-only in both ML repositories:

- do not edit files;
- do not append agent or experiment ledger events;
- do not run tests, training, evaluation, dataset, checkpoint, or GPU work;
- do not commit, sync, or repair differences;
- preserve and report pre-existing dirty state;
- write the final audit only in the Core workbench.

## Files to inspect in each repository

### Guaranteed instructions and runtime configuration

- `AGENTS.md`
- `.codex/config.toml`
- `.codex/agents/*.toml`

### Project direction and human-readable history

- the canonical roadmap;
- `PROJECT_LOG.md`;
- `README.md`;
- the project adapter or orchestration document;
- any document explicitly required by `AGENTS.md`.

### Agent and ML work evidence

- agent ledger and schema;
- agent-ledger tool;
- experiment ledger and schema;
- experiment-ledger tool;
- logging documentation;
- a small set of linked reports needed to reconstruct representative tasks.

### Repository evidence

- Git status and recent log;
- relevant changed or untracked orchestration files;
- repository-local Core lock, manifest, validator, or managed-file list when
  present.

## Audit questions

### 1. Instructions and context

- Which files are guaranteed to reach each agent?
- Which important rules exist only in documents an agent may never read?
- Where do `AGENTS.md`, profiles, configs, and task briefs duplicate or
  contradict one another?
- Which project-specific rules must remain outside universal Core?

### 2. Delegation and autonomy

- Did Terra usually complete a bounded task independently?
- How many routine failures caused unnecessary supervisor handoffs or retries?
- Was Luna used where direct Sol work would have been cheaper?
- Which stop conditions were useful, and which created premature returns?
- Can completed work be accepted from one worker report and its evidence?

### 3. Agent ledger

- Which fields were actually useful for reconstructing task, actor, outcome,
  checks, changed files, and stop reason?
- Which lifecycle events, metadata fields, reviews, and corrections created
  ceremony or failures?
- How often did logging itself require retries, corrections, or dedicated
  tasks?
- Would the simplified `agent_task_log_candidate.md` preserve the useful
  information in representative successful and failed tasks?

### 4. ML ledger and reports

- Which ledger entries helped locate a meaningful operation and its report?
- Which fixed fields duplicated detailed reports or forced tool/schema
  changes?
- Can the useful history be represented by a short summary, decision or
  limitation, and repository-relative links?
- Would `ml_work_log_candidate.md` work for both generative and classical ML
  without domain-specific fields?

### 5. Roadmap and PROJECT_LOG

- Can a new supervisor identify current state, completed stages, next approved
  work, and later ideas quickly?
- Are roadmap transitions explicit, or can an agent silently advance?
- Does `PROJECT_LOG.md` provide a useful milestone history without duplicating
  reports and ledgers?
- Are there duplicate headings, repeated summaries, oversized entries, or
  conflicting update instructions?
- Do `roadmap_file_candidate.md` and `project_log_file_candidate.md` cover the
  observed needs?

### 6. Cross-repository differences

- Which differences are legitimate project rules?
- Which differences are accidental drift in universal agent behavior or
  shared tools?
- Why did the two ledger tools and schemas diverge?
- Which files can be removed from the future foundation?
- Which repeated needs justify a standard document inside the initially empty
  `docs/` directory?

## Method

1. Record Git status and recent log for both repositories.
2. Build the explicit orchestration-file inventory.
3. Read guaranteed instructions and identify every required secondary file.
4. Summarize ledger structure and event counts with read-only commands.
5. Select a small representative set of cases:
   - one autonomous successful worker task;
   - one failed or interrupted task;
   - one task where logging or review caused extra work;
   - one meaningful ML operation from each repository.
6. Trace each case from task and agent evidence to project log, roadmap,
   report, and decision.
7. Compare agent and experiment tools, schemas, and instructions across the
   repositories.
8. Test each current workbench candidate against the observed cases.
9. Produce one combined report with findings, retained requirements,
   removable complexity, and proposed candidate changes.

Use scripts only for deterministic read-only counting or comparison. Do not
build the future logging or synchronization system during the audit.

## Deliverable

Create one combined Core workbench report:

`workbench/ml_repositories_orchestration_audit.md`

It should contain:

- a short profile of each repository;
- the actual orchestration-file inventory;
- representative task traces;
- repeated problems and useful safeguards;
- legitimate project differences;
- accidental drift;
- candidate changes;
- the recommended minimal foundation file list.

Do not create separate reports unless the combined file becomes genuinely
unreadable.

## Acceptance

The audit is complete when it can answer:

1. what universal information the new system must preserve;
2. what current complexity can be deleted;
3. whether the two simplified log candidates are sufficient;
4. whether the roadmap and project-log candidates reconstruct project state;
5. which standard documents, if any, belong in `docs/`;
6. what exact bounded implementation task should be given to Terra.
