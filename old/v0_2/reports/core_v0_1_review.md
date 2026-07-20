# Core v0.1 acceptance review

## Verdict

**Accept.** The repaired Core meets the bounded v0.1 acceptance checks. The
bundled validator is correctly documented as support for this repository's
schema vocabulary, not as a full Draft 2020-12 implementation.

## Evidence

- Target historical ledger plus this review's new `started` event validated:
  `python tools/agent_ledger.py validate` reported `valid: 6 events` before
  this review's terminal event.
- `python -m unittest discover -s tests -v` passed all 8 tests; Core validator
  and `git diff --check` passed.
- An isolated real lifecycle `started -> completed -> reviewed` passed
  validation. Repeated start, terminal, and review each returned exit 2 and
  left the ledger byte-identical.
- Isolated invalid fixtures for a string `constraints`, unknown property, bad
  reasoning enum, invalid run-id pattern, and a non-string nested constraint
  were rejected before mutation.
- Empty-ledger first append worked. A pre-existing sidecar lock failed closed
  without creating the ledger; a successful append removed its lock sidecar.
  The recovery instruction is documented in `docs/agent_orchestration.md`.
- In an isolated Core copy, edits to mutable `PROJECT_LOG.md` and
  `ORCHESTRATION_ROADMAP.md` retained manifest validity. Tampering with the
  managed `tools/agent_ledger.py` was rejected as `manifest hashes differ`.
- An isolated bootstrapped adapter completed a full lifecycle and validated.
  `sync_core.py` dry-run was byte-identical; `--apply` refused with exit 2.
- `.gitignore` allowlists only project-local `.codex/config.toml` and agent
  profiles; Luna/Terra/Sol profiles match the approved routing levels.

## Scope

No ML operation, network install, source write, commit, push, or remote action
occurred. Source remained at
`de8e236083d68d40c997c61c811d84042d746290` with only its pre-existing
agent-ledger modification.
