# Core v0.1 build report

Source provenance: a controlled bootstrap task from the generative repository;
source lifecycle IDs are recorded by its ledger helper. No source history,
experiment ledger, model, dataset, checkpoint, output, private context, or
absolute local path was copied.

The target starts with an empty agent ledger. Source bootstrap lifecycle start:
`6432496b-e2f6-4406-ae95-daa8c24e875e`; the source terminal event is appended
after this report is finalized.

Actual checks from the target workdir:

```text
python tools/validate_orchestration.py --write-manifest
python -m unittest discover -s tests -v
python tools/validate_orchestration.py
python tools/agent_ledger.py validate
git diff --check
```

Results: five targeted tests passed; manifest, TOML, schema-shape, empty
ledger, temporary bootstrap adapter, standalone adapter validation, nonempty
target refusal, sync dry-run no-mutation, and sync `--apply` refusal passed.
v0.1 sync is dry-run-only by design; it does not claim an unproven safe write
path. No ML operation occurred.

## Bootstrap repair

Independent review exposed a real first-append failure. Reproduction used a
metadata JSON file and a temporary empty ledger, not shell-embedded JSON:
the unmodified helper returned `error: [Errno 13] Permission denied` and left
the temporary ledger at zero bytes. The cause was specific to the Windows
branch: `msvcrt.locking(..., LK_LOCK, 1)` attempted to lock a byte at EOF in a
zero-byte ledger. Windows rejected that lock.

The helper now locks a one-byte sidecar `ledger.jsonl.lock` before opening the
ledger. Thus a lock failure cannot create or mutate the ledger; only a locked
holder opens and appends at EOF. The sidecar is ignored by Git. The portable
reviewer command is:

```powershell
python tools/agent_ledger.py start --metadata-file task-start.json
```

Repair checks: seven targeted tests passed, including subprocess metadata-file
first start on an empty ledger, forced Windows lock failure with byte-identical
no-ledger result, and first start in a temporary bootstrapped adapter. The
target's actual `reports/agent_execution_ledger.jsonl` remains zero bytes.

## Acceptance rework

Lifecycle validation now evaluates ordered history, accepting a normal
start/completed/reviewed chain and rejecting duplicate starts, terminals, and
reviews. The bundled schema validator enforces the vocabulary used by the
shipped schemas; it is not presented as a complete JSON Schema implementation.
Atomic exclusive sidecar creation replaces advisory byte locking and cleans up
on normal success/failure; stale sidecars fail closed. The pre-fix sidecar was
removed only after a process check found no Python writer. Manifest hashing now
covers immutable distributed files (including schemas and tools) while
excluding operational logs, reports, ledgers, and roadmaps.

No ML operation occurred.

## Closeout

Supervisor acceptance event: `bd15516e-c61c-4a71-b09d-01e94459db7c`.
Core v0.1 is frozen. A separate sklearn adapter bootstrap and umbrella-chat
verification are next; neither was executed in this closeout.
