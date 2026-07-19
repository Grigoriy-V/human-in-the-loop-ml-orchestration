# Supervised Agent Project

This project was bootstrapped from Human-in-the-Loop Orchestration Core v0.2.
It contains a project-local agent ledger, bounded task contracts, routing
profiles, provenance validation, and adapter-owned policy.

Core v0.2 is an experimental personal proof of concept with nominal
reproducibility. It is not a production framework, compatibility promise, or
v1.0 release.

Start every repository task from a metadata file:

```powershell
python tools/agent_ledger.py start --metadata-file task-start.json
```

The root agent is supervisor-only. Workers operate within explicit scope and
record terminal evidence; only the supervisor records a reviewed decision.
Long-running, consequential, or externally mutating work remains human-gated.

Run local validation with:

```powershell
python -m unittest discover -s tests -v
python tools/validate_core_pin.py
python tools/agent_ledger.py validate
python tools/validate_orchestration.py
```

The adapter type, exact Core commit, immutable managed inventory, and hashes
are recorded in `orchestration.lock.json`. Mutable roadmaps, logs, reports, and
JSONL ledgers are intentionally outside the managed inventory.
