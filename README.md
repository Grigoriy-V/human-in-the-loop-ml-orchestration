# Human-in-the-Loop Orchestration Core

Core v0.2 is an experimental personal proof of concept for supervised,
auditable project agents. It targets nominal reproducibility for this
workspace; it is not a production framework, a compatibility promise, or
v1.0. It provides generic lifecycle governance, routing profiles, append-only
agent evidence, canonical bootstrap templates, explicit adapter overlays, and
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

This is an experimental personal v0.2 PoC, not a production framework or a
v1.0 freeze. `sync_core.py` remains dry-run only and `--apply` intentionally
returns exit 2 without mutation.

Any future sync should first compute a deterministic hash/diff over the
declared managed-file list. Only when differences exist may an agent be
invoked to prepare a proposed change for manual approval. Automatic apply is
out of scope.

See the [v0.2 technical report](reports/core_v0_2_candidate.md) and the
[multi-repository bootstrap case study](docs/case_studies/autonomous_multi_repo_bootstrap.md).
