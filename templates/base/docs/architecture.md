# Architecture

Core owns generic supervision, routing, lifecycle, ledgers, schemas, template
provenance, and validation. An adapter owns domain policy. A project owns its
mutable roadmap, logs, reports, ledgers, data policy, and decisions.

The managed-file manifest covers immutable template outputs only. Mutable
roadmaps, logs, reports, and JSONL ledgers are emitted but deliberately
excluded from Core pin coverage.
