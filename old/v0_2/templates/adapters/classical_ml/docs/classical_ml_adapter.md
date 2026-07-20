# Classical ML adapter

This overlay owns dataset identity and fingerprinting, target definition,
license evidence, leakage audit, split strategy, feature schema, sklearn
Pipeline structure, baseline and cross-validation evidence, calibration,
threshold selection, artifacts, and the resulting decision. Dataset selection,
download, training, and evaluation remain human-gated.

`tools/experiment_ledger.py` authoritatively enforces the exact
`bundled-classical-v2` vocabulary described by
`reports/experiment_ledger.schema.json`; no complete JSON Schema Draft
implementation is claimed.

Callers cannot supply `event_id` or `timestamp_utc`. The helper generates a
UUIDv4 and system UTC, takes an atomic sidecar lock before opening the ledger,
validates all history plus the candidate, enforces experiment identity and
stage lifecycle, and verifies contained regular non-link artifact bytes.
Existing locks fail closed. Validation errors clean the lock without changing
ledger bytes.

A process crash or uncertain append deliberately retains the lock. Confirm no
writer remains, preserve lock metadata, validate the JSONL tail, and remove the
sidecar only when the ledger is complete and valid. Never rewrite history to
hide a corrupt tail.
