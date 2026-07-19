# Core v0.2 template and provenance candidate

## Current status

**Accepted as a v0.2.0 candidate.** Supervisor events
`5d407234-db43-484c-86e9-7d6d61884765` and
`5714c98f-e1d2-48c9-be15-46bdf9de05e3` accepted the implementation and the
independent technical review. This acceptance does not freeze v1.0.

The next milestone is a separate clean-commit release gate before any v1.0
freeze decision. `sync_core.py --apply` remains deferred and unavailable.

## Initial worker verdict

**Ready for independent review as a v0.2.0 candidate.** This worker does not
accept or freeze the release. Core remains dirty and uncommitted for one
independent supervisor review.

## Delivered boundary

Bootstrap inputs are no longer embedded as project-file strings in
`tools/bootstrap_project.py`. `templates/base` is the universal source and
`templates/adapters.json` declares exactly two overlays:

- `generic`: orchestration-only output with 24 immutable managed files and
  three mutable seeds. It has no ML roadmap, experiment helper/schema/ledger,
  or classical test.
- `classical_ml`: the same generic base, explicit `AGENTS.md` and `.gitignore`
  replacements, and classical docs/helper/schema/tests. It has 28 immutable
  managed files and five mutable seeds.

The classical overlay preserves supervisor-only control, Luna `none`, Terra
`low`, Sol `high`, privacy boundaries, the semi-automatic human gate for long
training/evaluation, and the accepted audit-grade experiment contract.

Official bootstrap now requires a clean Git worktree and exact lowercase
40-hex `HEAD`. It copies through a private temporary directory, verifies the
emitted local pin, and only then renames into a previously nonexistent target.
Unknown adapters, dirty Core, unsafe sources, existing targets, copy/hash
failures, and invalid emitted pins fail closed.

Every target receives a closed `orchestration.lock.json` with Core repository,
version, exact commit, adapter identity, exact managed inventory,
`base_copy`/`overlay_copy` relationship, and Core/target SHA-256. The target
validator uses the adapter-specific immutable `core/managed_files.json`,
requires exact coverage and unique canonical paths, verifies target bytes,
containment, regular-file status, and symlink/junction/reparse-free parents.
Optional `--core-root` also checks Core VERSION, commit, and every source hash.

Core's refreshed immutable manifest contains 60 hashed files. Live
`ORCHESTRATION_ROADMAP.md`, `PROJECT_LOG.md`, `reports/*.md`,
`reports/*.jsonl`, and lock sidecars are declared mutable and excluded. Target
pins likewise exclude roadmaps, logs, reports, and ledgers while retaining
immutable tools, profiles, schemas, docs, tests, and template declarations.

## Verification

Commands actually run:

- `python -m py_compile tools/bootstrap_project.py tools/validate_orchestration.py tools/sync_core.py templates/base/tools/agent_ledger.py templates/base/tools/validate_core_pin.py templates/base/tools/validate_orchestration.py templates/adapters/classical_ml/tools/experiment_ledger.py tests/test_core.py templates/base/tests/test_scaffold.py templates/adapters/classical_ml/tests/test_classical_contract.py`
  — passed.
- `python tools/validate_orchestration.py --write-manifest`
  — wrote 60 immutable hashes.
- `python tools/validate_orchestration.py`
  — passed.
- `python -m unittest discover -s tests -v`
  — 9 Core tests passed, 0 failures/skips.
- `python run_matrix_temp.py`
  — from isolated clean committed snapshot
  `dff6162c1a2b263c856482b727c11ce6221b988c`: generic target 3/3 and
  classical target 13/13 passed; local+explicit pins and both target
  orchestration validators passed. The temporary script and workspace were
  removed afterward.
- `python tools/bootstrap_project.py --dry-run --target ../dirty-core-refusal-probe --adapter-type generic --adapter-name DirtyProbe`
  — exit 2 as required on the dirty development Core; no target was created.
- `python tools/agent_ledger.py validate`
  — passed before terminal event.
- `git diff --check`
  — passed.

The nine Core tests create a fresh committed Core snapshot per case and cover:
unknown adapter, clean dry-run, dirty-source refusal, generic/classical
inventories, both target suites, full PowerShell
`start --metadata-file -> completed -> reviewed` lifecycle, local/explicit
pins, managed target/source tamper, traversal, duplicate/missing/extra/nonhex
pin entries, wrong commit, symlink file and parent, mutable-target and
mutable-Core edits, managed-template tamper, sync dry-run byte identity,
`--apply` refusal, and absence of inline project files or sibling dependencies.

Read-only before/after evidence for adapters was unchanged:

- classical: clean `11dff82d2c34a2deba09ae9596a5ab5f6099df65`,
  agent-ledger SHA-256
  `470745f8c91a3e4801c0918b49289c7584e47720b6c83d84956664e92fff933d`;
- generative: clean `c682ed1885fc83e5abdfeea305fe9da793f4b589`,
  agent-ledger SHA-256
  `b139d72d913af0d4dd163c043adbc1fe8d9314f9873e8a44e5b6fb6032de5aff`.

## Changed files

Core runtime and policy:

`AGENTS.md`; `ORCHESTRATION_ROADMAP.md`; `PROJECT_LOG.md`; `README.md`;
`VERSION`; `core/orchestration_lock.schema.json`;
`core/project_manifest.schema.json`; `docs/agent_orchestration.md`;
`docs/architecture.md`; `docs/project_adapter_contract.md`;
`orchestration_manifest.json`; `reports/agent_execution_ledger.jsonl`;
`reports/core_v0_2_candidate.md`; `tests/test_core.py`;
`tools/bootstrap_project.py`; `tools/sync_core.py`; and
`tools/validate_orchestration.py`.

Canonical template inventory:

`templates/adapters.json`;
`templates/adapters/generic/core/managed_files.json`;
`templates/adapters/classical_ml/.gitignore`;
`templates/adapters/classical_ml/AGENTS.md`;
`templates/adapters/classical_ml/ML_PROJECT_ROADMAP.md`;
`templates/adapters/classical_ml/core/managed_files.json`;
`templates/adapters/classical_ml/docs/classical_ml_adapter.md`;
`templates/adapters/classical_ml/reports/experiment_ledger.schema.json`;
`templates/adapters/classical_ml/tests/test_classical_contract.py`;
`templates/adapters/classical_ml/tools/experiment_ledger.py`;
`templates/base/.gitignore`; `templates/base/AGENTS.md`;
`templates/base/PROJECT_LOG.md`; `templates/base/PROJECT_ROADMAP.md`;
`templates/base/README.md`; `templates/base/VERSION`;
`templates/base/requirements.txt`; `templates/base/.codex/config.toml`;
`templates/base/.codex/agents/luna_clerk.toml`;
`templates/base/.codex/agents/sol_specialist.toml`;
`templates/base/.codex/agents/terra_worker.toml`;
`templates/base/core/orchestration_lock.schema.json`;
`templates/base/core/project_manifest.schema.json`;
`templates/base/core/task_spec.schema.json`;
`templates/base/docs/agent_orchestration.md`;
`templates/base/docs/architecture.md`;
`templates/base/docs/lesson_promotion.md`;
`templates/base/docs/lifecycle.md`;
`templates/base/docs/multi_repo_supervision.md`;
`templates/base/docs/project_adapter_contract.md`;
`templates/base/reports/agent_execution_ledger.schema.json`;
`templates/base/tests/test_scaffold.py`;
`templates/base/tools/agent_ledger.py`;
`templates/base/tools/validate_core_pin.py`; and
`templates/base/tools/validate_orchestration.py`.

## Limits and deferred work

This is not v1.0 and not an accepted freeze. `sync_core.py --apply` remains an
intentional exit-2/no-mutation path. Version propagation, conflict detection,
and safe upgrades of existing adapters are deferred.

Bootstrap creates new targets only; it does not update an existing adapter.
The pin uses the repository's current 40-hex Git object format. Local pin
validation proves target consistency with recorded immutable declarations;
source-checkout authenticity additionally requires explicit `--core-root`.
Bundled schema validators do not claim complete JSON Schema Draft support.
The classical experiment helper deliberately retains its lock after an
uncertain write so a human can inspect the tail; it never auto-repairs JSONL.

No data, ML operation, network action, commit, or push occurred. No approved
stop condition was encountered.

## Independent technical acceptance review

### Verdict: accept

The v0.2.0 candidate passed independent technical review with no material
blocker:

- all 9 Core tests, Core manifest/orchestration validation, and the complete
  Core agent ledger passed;
- a separate clean committed snapshot bootstrapped both adapters: generic
  inventory `24 managed / 3 mutable`, classical inventory
  `28 managed / 5 mutable`; local and explicit pins, target validators, target
  suites, generic PowerShell metadata-file lifecycle, and classical experiment
  contract all passed;
- generic output contained no classical helper, schema, ledger, roadmap, test,
  or adapter rules; classical output retained the exact semi-automatic
  user-launch gate;
- dirty Core, unknown adapter, existing target, pin/hash/path/relation/tamper
  failures, and linked file/parent paths failed closed without partial target
  output;
- mutable logs, roadmaps, reports, and ledgers remained outside immutable
  manifests, while managed tamper was rejected;
- sync dry-run was byte-identical and `--apply` returned 2 without mutation.

Core's immutable manifest contains 60 entries and validates all template,
tool, config, schema, and immutable documentation sources. The candidate is
explicitly v0.2.0 rather than a v1.0 freeze. No private path, secret, sibling
runtime dependency, data/model artifact, or large generated output was found.

Adapter evidence remained unchanged:

- classical commit `11dff82d2c34a2deba09ae9596a5ab5f6099df65`,
  ledger SHA-256 `470745f8c91a3e4801c0918b49289c7584e47720b6c83d84956664e92fff933d`;
- generative commit `c682ed1885fc83e5abdfeea305fe9da793f4b589`,
  ledger SHA-256 `b139d72d913af0d4dd163c043adbc1fe8d9314f9873e8a44e5b6fb6032de5aff`.

No ML, data, network, production-repository commit, or push occurred.
