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

The local helper generates UTC timestamps and event IDs, validates schema and
lifecycle transitions before append, requires explicit terminal commands and
changed-file evidence, and rejects absolute paths and secret-like values. It
uses an exclusive sidecar lock; a stale `.lock` fails closed and may be removed
only after confirming no writer process remains. Its bundled validator supports
the schema vocabulary used here; it is not a claim of full Draft 2020-12
implementation.

Bootstrap sources live under `templates/base` and declared adapter overlays.
Official bootstrap requires a clean committed Core checkout. The emitted pin
records exact source commit, managed inventory, relationships, and hashes.
Mutable roadmaps, logs, reports, and ledgers remain project-owned.

`sync_core.py --apply` is intentionally unavailable in the v0.2 candidate;
version propagation and conflict-aware mutation remain deferred.
