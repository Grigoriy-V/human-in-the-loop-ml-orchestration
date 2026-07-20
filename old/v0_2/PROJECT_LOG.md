# Project Log

This file records important completed milestones and decisions. Add one dated
entry after a material result, not after every task or test. Keep one heading,
summarize Outcome and Decision, state the important limitation, and link to
detailed reports rather than copying their contents.

## 2026-07-19 — Core v0.1 build

The standalone Core was created and verified with no ML operation, dataset,
training, evaluation, GPU, commit, or push. Five targeted unit tests passed;
the validator and empty-ledger validation passed. See
`reports/core_v0_1_build.md`.

## 2026-07-19 — Bootstrap repair

Windows first-start locking was repaired and seven targeted tests passed. The
real Core ledger remains empty for the independent first reviewer event.

## 2026-07-19 — Acceptance rework

Lifecycle, bundled schema checks, fail-closed atomic locking, and immutable
manifest ownership were reworked. Eight targeted tests and validator checks
passed; no ML operation ran.

## 2026-07-19 — Core v0.1 accepted and frozen

Supervisor accepted Core v0.1. The next approved step is a separate sklearn
adapter bootstrap followed by umbrella-supervisor verification; neither ran.

## 2026-07-19 — Independent Core v0.1 review

No-ML review checks ran: seven targeted tests, validator, ledger validation,
bootstrap/sync smoke, manifest tamper negative, and an invalid-ledger fixture.
The fixture was incorrectly accepted and persisted in an isolated temporary
ledger, so the review verdict is **changes required**. See
`reports/core_v0_1_review.md`.

The post-review helper validation additionally rejected its own normal
started/completed lifecycle as a duplicate start; this is included in the
same report.

## 2026-07-19 — Core v0.1 acceptance re-review

The repaired lifecycle, bundled schema vocabulary checks, fail-closed sidecar
behavior, mutable manifest exclusions, bootstrap lifecycle, and sync refusal
were independently checked with no ML operation. The acceptance verdict is
**accept**; see `reports/core_v0_1_review.md`.

## 2026-07-19 — Autonomous multi-repo case study

Documented the evidence-backed Core extraction, generative adapter integration,
classical scaffold reviews and current unaccepted boundary. Documentation only;
no ML or repository publication operation ran.

## 2026-07-19 — Independent multi-repo case-study review

Commit/event claims and the 1:31:14.391005 evidence-window arithmetic were
confirmed. Review requires correction of an unrecorded specialist
start/interruption claim, an unverified user-observation sentence, and mojibake
arrows. See `reports/autonomous_multi_repo_bootstrap_review.md`.

## 2026-07-19 — Core v0.2.0 candidate technical acceptance

The 9-test Core suite, 60-file manifest, committed-snapshot bootstrap matrix,
generic/classical target suites, pins, lifecycle, experiment contract, and
sync refusal passed independent review. Technical verdict: **accept**. See
`reports/core_v0_2_candidate.md`.

## 2026-07-19 — Core v0.2.0 clean-commit release gate

A clean local Windows clone of committed HEAD failed immutable-manifest
validation: all 60 hashes differed because checkout CRLF bytes did not match
the LF working-tree hashes used to build the manifest. Release verdict:
**changes required**. See `reports/core_v0_2_release_gate.md`.

## 2026-07-19 — Core v0.2 candidate template promotion

Bootstrap project sources moved into canonical `templates/base` plus declared
`generic` and `classical_ml` overlays. Clean-commit provenance, exact managed
inventories, target-local pin validation, mutable boundaries, overlay
separation, PowerShell metadata-file lifecycle, and fail-closed negatives were
implemented.

Nine Core tests passed. From a separate committed snapshot, the generic target
passed 3/3 tests and the classical target passed 13/13, including its
audit-grade experiment contract. Core and target validators passed; dirty
source and sync `--apply` refused without mutation. Decision: ready for
independent review as a v0.2.0 candidate, not accepted or frozen as v1.0. See
`reports/core_v0_2_candidate.md`.

No data, ML, network, commit, or push operation ran.

## 2026-07-19 — Core v0.2.0 candidate accepted

Supervisor events `5d407234-db43-484c-86e9-7d6d61884765` and
`5714c98f-e1d2-48c9-be15-46bdf9de05e3` accepted the implementation and its
independent technical review. The accepted scope is the v0.2.0 candidate, not
a v1.0 freeze.

The next milestone is a separate clean-commit release gate before any v1.0
freeze decision. `sync_core.py --apply` remains deferred and unavailable. No
additional test suite, ML, data, network, tag, or push operation ran during
this closeout.

## 2026-07-19 — Core v0.2.0 CRLF portability rework

Added canonical LF checkout policy to Core and generated adapters after the
clean-clone release gate found 60/60 immutable hash mismatches under
`core.autocrlf=true`. Common binary formats are explicitly excluded from text
and eol conversion; managed bootstrap copies remain raw-byte-preserving and
hash-equal.

The focused autocrlf clone matrix passed with a clean clone, all 62 Core
manifest hashes, generic `25 managed / 3 mutable`, classical
`29 managed / 5 mutable`, local and explicit pins, exact copy relations,
CRLF-tamper rejection, and byte-stable binary handling. The full 10-test Core
suite passed. Decision: ready for targeted independent re-review, not accepted
as a release. Version remains `0.2.0`; sync apply remains unavailable. See
`reports/core_v0_2_release_gate.md`.

No adapter write, ML/data operation, network action, commit, tag, or push ran.

## 2026-07-19 — Core v0.2.0 personal-PoC finalization

Labeled v0.2.0 as an experimental personal proof of concept with nominal
reproducibility, not a production framework or v1.0. Documented future sync as
deterministic managed-list hash/diff first, agent invocation only for detected
differences, and manual approval with no automatic apply.

Generated roadmap ownership is now exclusive: generic has only
`PROJECT_ROADMAP.md`, classical has only `ML_PROJECT_ROADMAP.md`, and Core
retains `ORCHESTRATION_ROADMAP.md`. Inventories are generic
`25 managed / 3 mutable` and classical `29 managed / 4 mutable`.

The full 10-test Core suite and focused autocrlf clean-clone matrix each passed
once. Decision: hand off the dirty PoC state for one supervisor acceptance and
one later commit. Version remains `0.2.0`; no adapter write, production commit,
tag, push, network, ML, or data operation ran.

## 2026-07-20: Simplified instruction foundation

### Outcome

Replaced the active Core `AGENTS.md`, runtime config, and Terra/Luna/Sol
profiles with the agreed supervisor-worker model. Updated the Core README and
the corresponding base Markdown/config templates. Terra now uses reasoning
`medium`; mandatory context must arrive through `AGENTS.md`, the active
profile, or the explicit task.

No logging or bootstrap code was implemented, and the old implementation has
not yet been removed.

### Decision

Use one future `work_log.py` with separate agent and ML journals. Test the new
foundation before switching the remaining Core implementation and deleting
the old lifecycle, adapter, lock, manifest, and sync machinery. Automatic
context-compaction config remains deferred because the proposed runtime keys
were not confirmed locally.
