# Project adapter contract

An adapter is self-contained at runtime. A fresh Codex chat loads only the
applicable `AGENTS.md` and project configuration found for the repository it
opens. It does not inherit live instructions from a sibling Core checkout,
another ML repository, or a previous chat.

Every adapter must therefore physically contain its complete common
supervisor/worker/audit rules, Luna/Terra/Sol profiles, local tools and
documentation, schemas, ledgers, roadmap, log, Core pin, and managed-file
declaration. Core is a reference, provenance record, and project template. It
is never required to be present or readable while an adapter runs.

## Local common and domain responsibilities

| Responsibility | Required locally in every adapter | Generative ML adapter owns | Classical ML adapter owns |
| --- | --- | --- | --- |
| Agent control | Supervisor-only decisions, bounded workers, Luna `none`, Terra `low`, Sol `high`, one local agent helper, audit evidence, and human gates | Same common local contract | Same common local contract |
| Data protocol | Local provenance and privacy rules | Dataset preparation, caches, checkpoint lineage, and sampling inputs | Dataset identity, source/license, target and positive class, label timing, leakage audit, and frozen split protocol |
| Modelling protocol | Human approval for long or consequential ML operations | Generic diffusion training/resume/sampling evidence and image-generation metrics | Fold-safe `sklearn` Pipeline, cross-validation, baselines, calibration, and decision-threshold protocol |
| Experiment evidence | Append-only local evidence with actual commands, hashes, artifacts, results, and decisions | Dataset/cache/checkpoint/sampling/image-metric events through its local experiment mechanism | Classical dataset/split/pipeline/CV/calibration/threshold events through its domain experiment helper |

Adapters that maintain an experiment ledger or perform material ML operations
must prohibit manual JSONL writes and provide a local experiment helper or
documented local append API. Agent lifecycle events must use the adapter's
local agent helper, and material experiment events must use that local
experiment mechanism. A missing or failing required helper is a stop condition,
not permission to patch ledger history. Core does not impose a universal ML
schema or experiment helper.

In v0.2 bootstrap, the entire immutable target-file inventory is declared in
`core/managed_files.json` and pinned in `orchestration.lock.json`. Generic
files come from `templates/base`; adapter additions or replacements come from
one explicit declared overlay. `base_copy` and `overlay_copy` are byte-identical
relationships whose target and Core source hashes must match.

Mutable roadmaps, logs, reports, and JSONL ledgers are target-owned and never
appear in the managed inventory. Domain overlays may add policy but may not
weaken supervisor-only control, lifecycle evidence, privacy, or human gates.

This candidate does not implement sync application. Future propagation must
detect versions and conflicts, preserve adapter-owned mutable content, and
remain human-reviewed before `--apply` can be enabled.
