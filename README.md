# Human-in-the-Loop Orchestration Core

Core v0.2 is a candidate release for supervised, auditable project agents. It
provides generic lifecycle governance, routing profiles, append-only agent
evidence, canonical bootstrap templates, explicit adapter overlays, and
machine-verifiable source provenance. It has no ML framework, dataset, GPU, or
network dependency.

## Declared adapters

- `generic`: universal orchestration-only scaffold. It contains no domain or
  ML experiment ledger.
- `classical_ml`: generic base plus classical-ML rules, human-gated long-run
  policy, and the audit-grade experiment helper/schema/tests.

Bootstrap reads project files only from `templates/base` and the selected
`templates/adapters/<type>` overlay. Mutable roadmaps, logs, reports, and
JSONL ledgers are emitted but excluded from managed pin coverage.

## Validation

```powershell
python -m unittest discover -s tests -v
python tools/agent_ledger.py validate
python tools/validate_orchestration.py
git diff --check
```

Official bootstrap requires a clean committed Core checkout and records its
exact commit and hashes. From such a checkout:

```powershell
python tools/bootstrap_project.py --target <new-directory> --adapter-type generic --adapter-name Example
python tools/bootstrap_project.py --target <new-directory> --adapter-type classical_ml --adapter-name Example
```

The test suite creates an isolated committed Core snapshot for positive
bootstrap tests. There is no dirty-source bypass.

For the first ledger event, use a metadata file:

```powershell
python tools/agent_ledger.py start --metadata-file task-start.json
```

## Candidate boundary

This is a v0.2 candidate, not a v1.0 freeze. `sync_core.py` remains dry-run
only. `--apply` intentionally returns exit 2 without mutation; conflict-aware
version propagation and apply are deferred to a later reviewed milestone.

See the [v0.2 technical report](reports/core_v0_2_candidate.md) and the
[multi-repository bootstrap case study](docs/case_studies/autonomous_multi_repo_bootstrap.md).
