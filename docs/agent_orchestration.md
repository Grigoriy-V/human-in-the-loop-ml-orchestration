# Agent orchestration

This is the Core entrypoint. Read [architecture](architecture.md) for the Core
boundary, [lifecycle](lifecycle.md) for ledger events,
[multi-repository supervision](multi_repo_supervision.md) for umbrella-chat
boundaries, [the adapter contract](project_adapter_contract.md) for local
ownership, and [lesson promotion](lesson_promotion.md) for controlled reuse.

Use a metadata file for the first ledger event:

```powershell
python tools/agent_ledger.py start --metadata-file task-start.json
```

Core v0.2 uses bundled validators for the schema vocabulary shipped here
(`required`, types, properties, arrays, enums, patterns, constants and the
conditional forms used by the ledger). It is not a claim of full Draft 2020-12
implementation. A stale `.lock` sidecar fails closed; remove it only after
confirming no writer process remains.

Bootstrap sources live under `templates/base` and declared adapter overlays.
Official bootstrap requires a clean committed Core checkout. The emitted pin
records exact source commit, managed inventory, relationships, and hashes.
Mutable roadmaps, logs, reports, and ledgers remain project-owned.

`sync_core.py --apply` is intentionally unavailable in the v0.2 candidate;
version propagation and conflict-aware mutation remain deferred.
