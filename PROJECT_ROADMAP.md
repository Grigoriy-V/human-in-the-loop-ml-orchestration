# Core Project Roadmap

**Updated:** 2026-07-20

**Project status:** foundation accepted

**Current approved step:** none

This is the single source of accepted Core direction. Discussion and roadmap
edits do not authorize implementation. Work proceeds one approved step at a
time after an explicit human command.

## Current state

- Active agent instructions, config, profiles, README, roadmap, and
  PROJECT_LOG use the accepted minimal model.
- The active root contains empty `docs/`, `tools/`, and `tests/` directories,
  two empty work journals, and `workbench/`.
- The previous v0.2 implementation is isolated under `old/v0_2/` and is not
  active.
- `work_log.py` has not been implemented.
- Bootstrap, adapters, comparison tooling, and ML-repository migration are
  deferred.

## Completed steps

### 1. Discuss and audit the new operating model

- **Result:** roles, context, logging, roadmap, project-log, and repository
  foundation decisions were recorded.
- **Evidence:** `workbench/` and
  `workbench/ml_repositories_orchestration_audit.md`.
- **Decision:** replace the old lifecycle and adapter-oriented design.
- **Limitation:** no new implementation was produced.

### 2. Establish and accept the clean Core foundation

- **Result:** created the new active files and isolated the old system in
  `old/v0_2/`; a fresh Terra contract smoke-test passed.
- **Evidence:** repository tree and `PROJECT_LOG.md`.
- **Decision:** accept the minimal foundation as the active Core baseline.
- **Limitation:** the logging tool does not exist and no active implementation
  test suite exists yet.

## Next candidates

Candidates are not authorized merely because they are listed.

1. Discuss and implement the minimal `work_log.py`.
2. Add project documentation or connected-project profiles only when a
   concrete need is accepted.

## Later ideas

- Update the generative and classical ML repositories separately.
- Analyze repeated agent errors and incidents.
- Reconsider a read-only comparison tool after the repositories are aligned.
- Use native resource reporting and automatic context compaction only if the
  runtime exposes simple reliable support.

## Maintenance

When a step closes, record result, evidence, decision, and limitation. Clear
the current step and discuss the next transition before authorizing more work.
