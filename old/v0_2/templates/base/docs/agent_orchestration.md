# Agent orchestration

This project is a self-contained adapter generated from Core v0.2. Read
[architecture](architecture.md) for boundaries, [lifecycle](lifecycle.md) for
ledger events, [multi-repository supervision](multi_repo_supervision.md) for
repository isolation, [the adapter contract](project_adapter_contract.md) for
local ownership, and [lesson promotion](lesson_promotion.md) for controlled
reuse.

PowerShell starts use a metadata file:

```powershell
python tools/agent_ledger.py start --metadata-file task-start.json
```

The bundled agent-ledger validator implements only the vocabulary used by its
shipped schema; it does not claim full JSON Schema Draft support. A stale
sidecar lock fails closed. Remove it only after confirming that no writer
process remains.

Core v0.2 records exact source commit and managed hashes at bootstrap.
`sync_core.py --apply` remains intentionally unavailable; automatic version
propagation and conflict-aware application are deferred.
