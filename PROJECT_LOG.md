# Project Log

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
