# Core v0.2.0 clean-commit release gate

## Verdict

**Changes required.** The committed candidate does not pass its own immutable
manifest validation in a clean local clone on Windows.

## Blocking evidence

The review cloned local committed HEAD
`7e9a6f26fcc486a3bf5dcfddb4f49e76a7ee2cd1` with no network. The clone was
clean (`git status --porcelain` empty) and reported `VERSION` `0.2.0`, but:

```text
python tools/validate_orchestration.py
manifest: immutable manifest hashes differ
```

Independent recomputation found mismatches for all 60 immutable entries.
The clone inherited `core.autocrlf=true`; checkout bytes were CRLF while the
manifest contains hashes computed from the original LF working-tree bytes.
Git still reports the clone clean, so the manifest currently validates one
working-tree line-ending representation rather than the committed portable
content.

Representative mismatches:

- `VERSION`: expected `1f930dd1...`, clean clone `c58a749f...`;
- `tools/bootstrap_project.py`: expected `16b71353...`, clone `f3eb4748...`;
- `templates/base/tools/agent_ledger.py`: expected `0269109b...`, clone
  `5385a15d...`;
- `templates/adapters.json`: expected `6179b104...`, clone `b94f81f8...`.

Because clean-clone manifest validation is a prerequisite, the official
bootstrap release matrix was stopped before promotion. The earlier candidate
suite and dirty-source refusal remain useful evidence, but they cannot replace
validation from committed checkout bytes.

## Scope

No implementation or documentation fix, adapter write, ML/data operation,
network access, production-repository commit, tag, or push occurred.

## CRLF portability rework

The bounded rework adds repository and scaffold `.gitattributes` policies that
force detected text to LF while explicitly disabling text/eol conversion for
common binary formats. `.gitattributes` is itself immutable in Core and in
both generated adapter inventories.

Bootstrap continues to copy files without decoding or content normalization;
every managed source/target pair must have identical raw SHA-256 hashes. The
new regression creates a local committed clone with `core.autocrlf=true` and
proves:

- the clone is Git-clean and all 62 Core manifest hashes match checkout bytes;
- generic `25 managed / 3 mutable` and classical
  `29 managed / 5 mutable` targets bootstrap successfully;
- every managed target is byte-identical to its declared Core source;
- local and explicit-Core pin validation passes for both adapters;
- a one-line LF-to-CRLF tamper still fails pin validation;
- an explicit binary fixture remains byte-identical in an autocrlf clone and
  is classified with `text` and `eol` unset.

The focused release-clone regression and the complete 10-test Core suite
passed. This is corrective evidence for a targeted independent re-review, not
release acceptance. Version remains `0.2.0`; `sync_core.py --apply` remains a
refusal path. No adapter repository, ML/data operation, network action,
production commit, tag, or push occurred.

## Minimal personal-PoC finalization

Core v0.2.0 is explicitly an experimental personal proof of concept with
nominal reproducibility for this workspace. It is not a production framework,
compatibility promise, or v1.0 release.

Generated roadmap ownership is now singular:

- generic emits `PROJECT_ROADMAP.md` and not `ML_PROJECT_ROADMAP.md`;
- classical emits `ML_PROJECT_ROADMAP.md` and not `PROJECT_ROADMAP.md`;
- Core retains `ORCHESTRATION_ROADMAP.md`.

This changes only the classical mutable inventory:
generic remains `25 managed / 3 mutable`; classical is now
`29 managed / 4 mutable`. Both generated validators enforce the exclusive
roadmap boundary.

Future sync is documentation-only: first compute a deterministic hash/diff
over the declared managed-file list, invoke an agent only if differences
exist, then require manual approval. Automatic apply is out of scope and the
existing `--apply` refusal remains unchanged.

The complete 10-test Core suite and the focused autocrlf clean-clone bootstrap
matrix each passed once for this final state. Version remains `0.2.0`. This
state is handed off dirty for one supervisor decision and one later commit;
no separate reviewer is requested. No adapter write, production commit, tag,
push, network, ML, or data operation occurred.
