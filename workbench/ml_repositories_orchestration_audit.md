# Audit: orchestration experience in the two ML repositories

**Status:** completed read-only audit.
**Date:** 2026-07-20.
**Implementation authorization:** none.

## Executive conclusion

The two repositories confirm the intended direction of the Core redesign.

The useful system is:

```text
human discusses direction with Sol supervisor
-> human authorizes the next agreed step
-> supervisor gives one bounded result-oriented task
-> one worker owns implementation, diagnosis, retry, tests, and evidence
-> worker returns once with a complete result or one real blocker
-> supervisor reviews the result and reports the decision
```

The unsuccessful part is the infrastructure around that system:

- mandatory `started -> terminal -> reviewed` events for every task;
- large hand-written metadata payloads;
- logging tasks and reviews that exist only to maintain logging;
- schemas that force ML work into predefined domain-specific lifecycles;
- adapter pins, managed-file hashes, locks, and validators that create their
  own synchronization work;
- important rules repeated in `AGENTS.md`, profiles, orchestration documents,
  schemas, and helper behavior.

The current candidates are sufficient as the basis for implementation after a
small number of explicit decisions. Detailed ML evidence remains valuable, but
it belongs in project reports rather than in a universal fixed-field journal.

## Audit boundary

Repositories:

- Generative ML: `D:\ML\My_first_model`
- Classical ML: `D:\ML\product-conversion-ml-case`

The audit was read-only in both repositories. It did not:

- edit project files;
- append ledger events;
- run tests, validators, training, evaluation, datasets, checkpoints, or GPU
  work;
- commit, synchronize, or repair repository state.

Initial state:

| Repository | Branch and HEAD | Working tree |
| --- | --- | --- |
| Generative | `main`, `fce34a7` | Existing modification to `reports/agent_execution_ledger.jsonl`: six lifecycle events from two earlier Core audits |
| Classical | `main`, `b6afbbb` | Clean |

The generative dirty state is important evidence. Two read-only Core audits
created six `started`, `completed`, and `reviewed` records and left the ML
repository dirty. The current audit did not add to them.

## Repository profiles

### Generative ML

Purpose:

- train and evaluate generative image models;
- preserve checkpoint and evaluation lineage;
- compare models under frozen protocols;
- keep long GPU work human-gated.

Distinctive project requirements:

- do not commit datasets, checkpoints, or full generated outputs;
- use fixed seeds, sample budgets, sampler, CFG, VAE, feature extractor, and
  matched evaluation protocol where comparisons require them;
- distinguish quick and full evaluation, raw and EMA weights, and
  FID/KID versus precision/recall trade-offs;
- preserve checkpoint/config hashes and report limitations;
- account for Windows, Python environment, and GPU runtime details;
- the human launches consequential long training and evaluation commands.

These belong in the project's README, project instructions, task brief, and
ML reports. They do not belong in universal Core agent profiles or universal
log fields.

### Classical ML

Purpose:

- build a reproducible conversion-classification case;
- preserve data, split, leakage, validation, and final-test boundaries;
- document the work as an educational and portfolio case.

Distinctive project requirements:

- dataset source, license, identity, and fingerprint;
- observation unit, target timing, positive class, and prediction-time feature
  availability;
- duplicate, group, and target leakage audit;
- learned preprocessing inside a fold-safe pipeline;
- frozen train/validation/test protocol and untouched final test boundary;
- train-only comparison, calibration, and threshold selection where relevant;
- reports with metrics, uncertainty, error slices, artifacts, and limitations.

These are legitimate project rules. Fixed JSONL fields for sklearn pipeline
structure, calibration, thresholds, and operation order are not universal
agent or ML-log requirements.

## Actual orchestration and context file inventory

### Shared by both ML repositories

```text
AGENTS.md
README.md
ML_PROJECT_ROADMAP.md
PROJECT_LOG.md
.codex/config.toml
.codex/agents/terra_worker.toml
.codex/agents/luna_clerk.toml
.codex/agents/sol_specialist.toml
docs/agent_orchestration.md
tools/agent_ledger.py
tools/experiment_ledger.py
reports/agent_execution_ledger.jsonl
reports/agent_execution_ledger.schema.json
reports/experiment_ledger.jsonl
reports/experiment_ledger.schema.json
orchestration.lock.json
```

### Generative-only orchestration evidence

```text
docs/ml_experiment_logging.md
tools/validate_core_pin.py
reports/orchestration_core_baseline_audit.md
reports/orchestration_core_adapter_integration.md
reports/orchestration_agent_ledger_helpers.md
reports/experiment_ledger_helper.md
```

There is no concise generative adapter/profile document analogous to the
classical adapter. Generative-specific behavior is distributed across
`AGENTS.md`, the roadmap, reports, and logging documentation.

### Classical-only orchestration evidence

```text
docs/classical_ml_adapter.md
docs/project_adapter_contract.md
tools/validate_orchestration.py
tools/validate_core_pin.py
core/orchestration_lock.schema.json
core/project_manifest.schema.json
reports/bootstrap_classical_adapter.md
```

The classical repository has a visible project adapter document, but also has
more copied Core ownership and validation machinery.

### Guaranteed information paths

An agent can be expected to receive only:

1. the applicable `AGENTS.md`;
2. the selected active profile/config;
3. the supervisor's task specification;
4. exact files that one of those guaranteed sources explicitly requires for
   the task.

The mere existence of README, roadmap, PROJECT_LOG, a report, a ledger, an
adapter document, or an orchestration document does not guarantee that the
agent reads it.

Therefore:

- short universal rules must be complete in `AGENTS.md`;
- role-specific behavior must be complete in the active profile;
- task-specific context and required evidence files must be named in the task
  specification;
- an important project document must be named by one of those guaranteed
  sources, not merely stored in `docs/`.

## Cross-repository drift

The active configurations still agree on two threads, depth one, Luna `none`,
Terra `low`, and Sol `high`. Almost every other orchestration file differs.

| File | Generative size | Classical size | Assessment |
| --- | ---: | ---: | --- |
| `AGENTS.md` | 41 lines | 110 lines | Same role/lifecycle repeated at different detail; classical includes domain rules |
| Terra profile | 12 lines | 25 lines | Same role, different wording and completeness |
| Luna profile | 14 lines | 21 lines | Same role, different boundaries |
| Sol profile | 12 lines | 24 lines | Same role, different boundaries |
| `docs/agent_orchestration.md` | 37 lines | 78 lines | Duplicated lifecycle with repository-specific additions |
| `tools/agent_ledger.py` | 288 lines | 102 lines | Same event contract, materially different implementation and error behavior |
| agent schema | 51 lines | 9 compressed lines | Nearly same required fields, different conditional validation |
| `tools/experiment_ledger.py` | 336 lines | 854 lines | Different domain systems |
| experiment schema | 41 lines | 615 lines | Generative event model versus detailed classical database |
| `orchestration.lock.json` | 17 lines | 99 lines | Different pin/ownership systems |

Both repositories pin an older Core lineage rather than current Core
`7217bee`. This is historical evidence, not a defect that should be repaired
during the audit. It shows that managed-file pinning creates ongoing work and
cannot be the foundation of a small system.

## Agent ledger findings

### Counts

| Repository | Total | Started | Completed | Failed | Reviewed | Correction |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Generative | 136 | 54 | 53 | 2 | 18 | 9 |
| Classical | 135 | 51 | 41 | 10 | 33 | 0 |

Both ledgers require the same large record shape: agent/run identity, model,
reasoning, task type, roadmap step, scope, constraints, commands, changed
files, before/after commits, ML event IDs, result, supervisor decision,
duration, and notes.

Useful information:

- task and actor;
- final status and stop reason;
- changed files;
- checks and material commands;
- result and evidence links;
- relation to a meaningful ML operation;
- enough Git state to locate the work.

Ceremony:

- mandatory start before any result exists;
- the same static metadata repeated across events;
- separate supervisor review event;
- correction events caused by lifecycle metadata rather than project work;
- exact model/reasoning fields in every event;
- requiring logging for read-only audits and trivial documentation;
- logging the work needed to build, validate, review, and re-review logging.

The classical helper demonstrates the failure mode precisely. It expects 15
start metadata fields but returns only `start metadata missing required field`
without naming the missing field. The normal instructions and `--help` do not
give a short complete payload. This matches the roadmap-write incident that
started the redesign.

### Representative successful autonomy

Generative:

- run `afhq-early-stop-quick200-20260718`;
- Terra owned tests, the approved quick comparison, validation, evidence, and
  reporting;
- it linked three ML events and returned a consolidated result;
- the supervisor could decide from the report and evidence.

Classical:

- worker event `e8407782-8ee6-445a-904a-4e034c51accf`;
- reviewed event `1c5e7151-6d66-4ec3-bfd2-ba3c6f44c79d`;
- ML events `c43928a9...` and `a42cc9ae...`;
- `reports/online_shoppers_model_comparison.md`.

Terra completed one bounded train-only comparison, test, report, evidence, and
decision request. This is the desired operating pattern.

### Representative useful stop

Classical:

- worker event `aa7ca66b-5863-4606-bce9-5a0b2df064d3`;
- reviewed event `7821f197-c481-472d-8023-1a1b59d78672`;
- ML event `340cc8dc-4f27-4277-b981-eced50eabe32`.

The required sklearn package was unavailable. The worker did not install
packages or broaden scope without approval. This stop condition protected a
real environment/authority boundary and should remain.

Generative:

- `luna-availability-check-failed-20260718`.

The launcher requested unsupported reasoning `minimal` for Luna. The work did
not begin, then profile corrections, correction events, and a new availability
check were needed. The useful lesson is to keep executable profiles simple and
verified; the lifecycle records did not solve the underlying mismatch.

### Representative logging overhead

Generative:

- accepting one AFHQ milestone created a separate Luna clerical task and three
  lifecycle events only to record an already available decision;
- helper review later produced `started -> failed -> reviewed(change)`,
  rework, identity corrections, and another review;
- two later read-only Core audits added six events and dirtied the repository.

Classical:

- a completed baseline could not be appended after an earlier failed baseline
  in the same experiment lineage;
- recovery required another lineage, a repeated dataset audit, and at least
  six agent events around the ledger problem;
- roadmap step 7 accounts for 45 of the repository's 135 agent events.

Some step 7 stops were legitimate. The number still shows that the event
model records orchestration micro-phases rather than one worker outcome.

## ML ledger findings

### Generative

- 30 events across seven experiment lineages;
- 9 evaluations, 7 training milestones, 3 closeouts, 2 corrections;
- every event has 19 mandatory top-level fields and six runtime fields.

The valuable information is checkpoint/config identity, actual protocol,
result, limitation, decision, and report/artifact location. The problem is
requiring all of it in every event even when the canonical report already
contains it.

A useful case is
`afhq-cats-repa-early-stop-manual-training-20k-20260718`: it correctly says
that the human launched training, runtime was unknown, and checkpoint lineage
and hashes were verified. The closeout's `freeze` decision and quick-versus-
full limitation are durable information.

### Classical

- 10 events across four experiment lineages;
- 9 completed and 1 failed;
- an 854-line helper and a 615-line schema;
- fixed fields for dataset, leakage, split, features, pipeline, CV,
  calibration, threshold, artifacts, and decision;
- enforced lifecycle from dataset audit through baseline, evaluation, and
  closeout.

The detailed evidence is valuable for the report. As a universal journal, the
schema is counterproductive:

- completed baseline recovery required a new experiment lineage;
- the dataset audit had to be repeated to satisfy that lineage;
- model comparison became another lineage because the schema had no safe
  comparison operation;
- the log structure dictated the work structure.

### Decision

The simplified `ml_work_log_candidate.md` is sufficient as a universal index:

- concise operation;
- outcome or stop reason;
- decision and limitation;
- repository-relative report/artifact links;
- script-generated ID, UTC, repository, branch, and HEAD.

Metrics, hashes, configs, dataset identity, split details, checkpoints,
pipeline structure, and full commands stay in linked project reports. A
project may define a stricter report or evidence artifact where justified, but
must not extend the universal log with domain-specific fields.

## Roadmap and PROJECT_LOG findings

### Roadmaps

Both repositories have one canonical roadmap and generally preserve useful
project boundaries.

The generative roadmap clearly distinguishes completed stages, pause, next
work, and distant ideas. The classical roadmap clearly protects the final test
boundary and waits for human direction.

Both are larger than the operational need and mix:

- current state;
- maintenance rules;
- detailed completed history;
- future plan;
- domain ideas.

The `roadmap_file_candidate.md` preserves what the supervisor actually needs:

- project status;
- one current approved step;
- concise current state;
- completed result, evidence, decision, and limitation;
- unauthorized next candidates and later ideas;
- explicit human transition before another step.

Domain protocols and detailed plans belong in project documents or reports.

### PROJECT_LOG

Both logs are useful human-readable history and easier to scan than JSONL.

The generative log is 652 lines and has a second `# Project Log` heading at
line 597, after which its format changes. The classical log is shorter but
contains detailed validator, pin, recovery, and lifecycle history that belongs
in linked reports or Git.

The `project_log_file_candidate.md` addresses the observed failure:

- one heading;
- an embedded short maintenance rule;
- one dated milestone entry;
- normal minimum of Outcome and Decision;
- Goal only when useful;
- links instead of copied metrics, command output, and lifecycle detail.

Roadmap and PROJECT_LOG must not duplicate one another:

- roadmap: accepted present and future;
- PROJECT_LOG: important past milestones and decisions;
- agent log: individual worker outcomes;
- ML log: index of meaningful ML operations;
- reports: detailed evidence.

## Useful safeguards to preserve

Preserve:

- one worker owns overlapping mutable files, output lineage, split, model, or
  checkpoint lineage;
- the worker does the complete in-scope fix/test/retry loop;
- long, expensive, destructive, external, privacy-sensitive, and explicitly
  consequential actions remain human-gated;
- workers stop for real authority, scope, environment, data, leakage,
  immutable-protocol, or concurrent-write conflicts;
- exact evidence and limitations are required for acceptance;
- no secrets, private identifiers, datasets, checkpoints, or large artifacts
  enter shared logs;
- append-only writes use a small script rather than agent-written JSONL;
- a helper error names the exact missing/invalid input and does not require
  reading a schema;
- important instructions reach the agent through guaranteed sources.

Remove:

- routine stop on logging ceremony before the actual task starts;
- independent review for every normal task;
- a separate worker merely to edit one roadmap or workbench note;
- mandatory commit or ledger event for every small action;
- adapter overlays and Core-managed downstream files;
- automatic sync as a foundation responsibility.

## Candidate changes after audit

### Agent task log

The candidate is sufficient with these first-iteration decisions:

1. One record is written only by a worker at completion or stop.
2. A worker crash before the final call is not reconstructed automatically in
   v1. The supervisor records an incident only if the failure matters.
3. Worker-supplied fields remain: agent, task, status, result, checks.
4. Exact commands are not a universal required field. Important commands
   belong in the concise checks/result or linked report.
5. The script detects repository, workdir, branch, HEAD, changed files, ID,
   UTC, and version.
6. Initial retrieval supports `list`, `show`, and text `search`; filters can be
   added only after a real audit query requires them.
7. The normal rule and one working command example fit in `AGENTS.md` and
   `--help`.

### ML work log

The candidate is sufficient with these first-iteration decisions:

1. One record per meaningful ML run, comparison, investigation, or coherent
   closeout.
2. Worker-supplied fields: summary, result, decision/limitation, zero or more
   repository-relative links.
3. No metrics, checkpoint, dataset, framework, pipeline, or protocol fields.
4. The script supplies repository, branch, HEAD, ID, UTC, and version.
5. Initial retrieval supports `list`, `show`, and text `search`.

### Roadmap and PROJECT_LOG

Both candidates are sufficient. Their maintenance instructions should be
copied into the generated files. They are normal Markdown documents and do not
need append helpers, schemas, locks, or lifecycle validation.

### Context and profiles

- Terra should use the already discussed `medium` reasoning in the new
  candidate profiles.
- `AGENTS.md` must be short but complete for universal behavior.
- Profiles contain only role-specific execution boundaries.
- The task brief names every non-guaranteed file required for the task.
- No rule may rely on an agent discovering a useful document.
- Context-compaction behavior remains a candidate rule and must not be
  implemented until the actual runtime supports a reliable threshold signal.

## Recommended minimal foundation

The audit supports this generated project:

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
|   `-- work_log.py
`-- reports/
    |-- agent_tasks.jsonl
    `-- ml_work.jsonl
```

No additional standard document in `docs/` is justified yet. Bootstrap can
create the empty directory. Project-specific documents should appear only
after manual adaptation reveals a concrete need.

Core itself additionally needs:

```text
projects/
|-- generative_ml.md
`-- classical_ml.md

workbench/
`-- discussion candidates, incidents, and audit reports

tools/
`-- one future read-only file-difference script over an explicit list
```

The two `projects/*.md` files are read-only profiles of known repositories,
not adapter overlays and not copied into a new project.

## Complexity that should not survive the redesign

Unless a later accepted requirement proves otherwise, remove rather than
deprecate:

- current multi-event agent ledger and schema;
- current experiment ledgers and domain schemas from the Core template;
- adapter overlay selection during bootstrap;
- adapter ownership markers and managed-file contracts;
- Core pin/provenance/hash matrices;
- synchronization apply logic;
- duplicate orchestration/lifecycle documents;
- validators whose only purpose is enforcing the removed machinery;
- compatibility layers for the old event formats.

Historical evidence remains available in Git and the two existing ML
repositories. The redesign does not modify those repositories.

## Exact bounded implementation task for Terra

This is a proposed task specification only. It is not authorized by this
audit.

### Result

Replace the current Core bootstrap, template, ledger, adapter, ownership, and
sync machinery with the approved minimal universal foundation and two
read-only existing-project profiles.

### Owned repository and paths

Repository:

`D:\ML\human-in-the-loop-ml-orchestration`

Allowed changes:

- root `AGENTS.md`, `README.md`, `PROJECT_ROADMAP.md`, and `PROJECT_LOG.md`;
- `.codex/config.toml` and `.codex/agents/*.toml`;
- `templates/` or the simpler replacement template location;
- `tools/bootstrap_project.py`;
- new `tools/work_log.py` with separate agent and ML modes;
- `projects/generative_ml.md` and `projects/classical_ml.md`;
- focused tests for bootstrap and both log tools;
- removal of superseded adapter, ledger, schema, lock, manifest, sync,
  ownership, validation, and duplicate documentation files;
- concise workbench/PROJECT_LOG/roadmap completion records after acceptance.

The two ML repositories are read-only and must not be changed.

### Required behavior

1. Bootstrap takes a destination only and creates the exact minimal skeleton;
   it does not ask for an adapter.
2. Generated `AGENTS.md`, profiles, roadmap, and PROJECT_LOG are
   self-contained under the guaranteed-information rule.
3. Terra profile uses reasoning `medium`; Luna uses `none`; Sol specialist
   uses the approved high-reasoning profile.
4. `work_log.py agent` appends one final task record from simple arguments and
   generates technical metadata.
5. `work_log.py ml` appends one meaningful ML-work record with concise text
   and repository-relative links.
6. Both modes offer short help plus `add`, `list`, `show`, and `search`;
   validate paths, reject secret-like values, and report the exact bad input.
7. Normal use requires no schema reading, metadata file, hand-written JSON,
   start event, review event, correction event, or commit.
8. Markdown roadmap and PROJECT_LOG contain their own short update rules and
   are edited directly.
9. Existing Core machinery with no accepted need is deleted without
   compatibility layers.
10. No automatic downstream sync or write operation is implemented.

### Worker autonomy

Terra owns implementation, refactoring, deletion, focused tests, debugging,
and internal retry until the accepted behavior passes. It returns once with:

- changed and deleted files;
- exact tests/checks and results;
- a generated-project tree from a temporary destination;
- sample add/list/show/search output for both log tools;
- limitations and any decision that still needs the supervisor;
- one final simplified agent task record if the new tool is available at the
  end of the task.

It stops only for:

- a required behavior that conflicts with the approved design;
- unexpected user changes overlapping an owned path;
- a destructive action outside the listed Core paths;
- need to modify either ML repository;
- missing human approval for a consequential action.

It does not stop for routine implementation choices, fixable test failures, or
normal refactoring needed to satisfy the accepted result.

### Acceptance

The supervisor accepts only after verifying:

- the generated tree exactly matches the approved foundation;
- both tools work without schema or metadata-payload knowledge;
- fresh local instructions contain every mandatory universal rule;
- no adapter is required for bootstrap;
- no old lifecycle, managed-sync, or domain-schema requirement remains active;
- tests and `git diff --check` pass;
- the two ML repositories retain their original state.

## Decisions made after the audit

1. Small Markdown reports and the short `agent_tasks.jsonl` and
   `ml_work.jsonl` journals are normal repository evidence. They are committed
   and pushed unless they contain secrets, private data, or large artifacts.
   Detailed or heavy generated artifacts remain outside Git and are referenced
   from the reports.
2. Core uses the same minimal foundation that it generates for a new project.
   Core naturally has additional files for its own purpose, including
   `workbench/`, connected-project profiles, templates, implementation tests,
   and Core development documentation. These are additions around the same
   foundation, not a different orchestration system.
3. The read-only file-difference script is deferred. The work order is:
   first simplify Core and make its minimum reliable; then adapt the two ML
   repositories through separate approved work in those repositories; only
   after that decide whether a comparison script is still useful and what
   exact files it should compare.

No token accounting, automatic context threshold, downstream synchronization,
adapter overlay, or new domain schema should be added to this implementation
step.
