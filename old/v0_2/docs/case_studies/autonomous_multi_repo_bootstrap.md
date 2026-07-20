# Case study: autonomous multi-repository bootstrap

## Starting point

The session began with one established generative-ML repository and a practical
question: how to extract reusable agent orchestration into a standalone Core,
prove that the extraction did not regress the existing project, and bootstrap a
second repository without collapsing all work into one chat or one Git history.

The target architecture separated:

- a human-controlled supervisor that defines scope and accepts or rejects
  milestones;
- bounded workers that own implementation and validation;
- independent reviewers that run adversarial checks;
- project-local adapters, Git histories, roadmaps and ledgers;
- human gates for long or consequential ML operations.

The umbrella chat coordinates repositories. It does not replace project chats
or merge their ledgers and commits.

## What the session produced

| Phase | Evidence-backed result | Decision |
| --- | --- | --- |
| Migration plan and baseline | Core/adaptor boundaries, regression gates and append-only audit requirements were recorded in the generative roadmap. | Accepted |
| Core v0.1 | Standalone lifecycle, routing profiles, ledger helper, validation, bootstrap, dry-run sync and documentation were created. | Accepted after rework; commit `14b7c25` |
| Generative adapter integration | Core version and managed files were pinned locally; no-ML regression and path-containment checks passed. | Accepted after two review/rework cycles; commit `5ed6ffb` |
| Classical adapter bootstrap | A separate classical-ML scaffold, local profiles, roadmaps and ledgers were created without data or model work. | Not accepted; repository remains uncommitted |
| Classical adversarial review | Review found incomplete pin validation and an experiment-ledger contract that could accept malformed evidence. | Changes required; bounded specialist escalation was proposed, but no specialist lifecycle was recorded before the human stop |

Core acceptance was recorded by event
`bd15516e-c61c-4a71-b09d-01e94459db7c`. Generative integration was accepted by
`c1377a3a-903d-4eae-9e6b-bfdc71012829`. The latest classical review decision,
`129ba674-1927-4e7c-a36e-859b07b53619`, remains `change`.

## Review discoveries that changed the implementation

The useful result was not merely that checks passed. Review repeatedly found
places where plausible-looking infrastructure was weaker than its claims:

1. A lifecycle validator rejected its own normal
   `started -> completed -> reviewed` history while accepting an invalid schema
   fixture.
2. Schema files existed, but early validation enforced only their shape rather
   than the actual field contracts.
3. Locking an empty ledger on Windows failed at EOF. The repair moved to
   fail-closed atomic sidecar creation and tested stale-lock behaviour.
4. The first manifest hashed mutable operational logs and reports, making
   legitimate append-only work look like tampering.
5. The first source integration pin was descriptive rather than
   machine-verifiable.
6. A later pin validator checked hashes but still allowed a managed path to
   escape through a symlink. Review added resolved-containment and
   symlink/reparse checks.
7. The classical scaffold listed the right concepts, but its experiment helper
   did not yet enforce a complete nested evidence contract, duplicate identity,
   artifact safety or lifecycle semantics.

This sequence matters:

```text
worker result -> independent review -> supervisor change
-> bounded rework -> adversarial re-review -> accept or change
```

It prevented a passing test count or a present schema file from being treated
as proof that the underlying safety property was real. Core moved from
`change` event `054c4bba-4ae1-4c50-972c-5db1315d0bcf` to acceptance only after
the lifecycle, schema, lock and manifest findings were addressed. The source
pin likewise passed only after `4eba2aea-cafe-425c-99c5-7582c715ae99` exposed a
decorative pin and `692ec7b3-e799-48ac-9e36-ecf9ec1bf61e` exposed path escape.

## Duration and evidence window

Conversation/session context supplied by the user says the autonomous session
was observed for more than one hour. This statement is not repository evidence.

Separately, the repository ledgers provide a narrower, exact evidence window
for this migration: from the roadmap-migration start at
`2026-07-18T19:44:50.0875052Z` to the latest recorded classical review decision
at `2026-07-18T21:16:04.478510Z`. That interval is exactly
**1:31:14.391005** (1 hour, 31 minutes, 14.391005 seconds). It is an
event-to-event evidence window, not a claim about the complete wall-clock
duration of the user's session.

## Safety boundaries

The migration and scaffold work did not run training, evaluation, sampling,
benchmarks, dataset preparation or downloads. Generative checkpoints, outputs
and the experiment ledger were kept outside the mutable integration scope.
Long ML remained human-gated. No repository was pushed during these
milestones, and each repository retained its own Git history, ledger and
working directory.

## Current status and next work

Core v0.1 and the generative adapter integration are accepted and committed.
The classical repository is intentionally uncommitted and not accepted. Its
latest review requires a stricter Core-pin schema and a genuinely enforced
classical experiment-ledger contract. The supervisor proposed a bounded Sol
specialist follow-up, but no specialist lifecycle or result was recorded before
the human stop.

The next work is therefore bounded:

1. finish the classical validator and ledger contract;
2. run a fresh independent acceptance review;
3. commit the classical scaffold only after acceptance;
4. verify the umbrella/superchat view across all repositories;
5. keep generative experiments paused until the migration gates are closed.

## Why this is a useful engineering case

This case shows how autonomous work can remain inspectable while spanning
multiple repositories. The important mechanism is not agent count. It is the
combination of narrow ownership, append-only evidence, explicit human
decisions, adversarial review and refusal to promote an attractive scaffold
before its safety claims are actually enforced.

It also shows a practical boundary for automation: the system made sustained
progress without ML or publishing side effects, while the human retained the
ability to stop work and leave an unaccepted repository uncommitted.
