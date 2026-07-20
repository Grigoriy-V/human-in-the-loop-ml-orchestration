# Candidate: Core scope and new-project foundation

**Status:** discussion draft only.
**Implementation authorization:** none.

## Core purpose

The repository exists to:

1. preserve and improve a compact human-in-the-loop agent system;
2. create a minimal agent foundation and folder skeleton for a new repository;
3. keep reusable agent and ML work-log tools;
4. inspect agent work in existing ML repositories and promote useful lessons;
5. serve as a small roadmap and workbench for orchestration development.

Core does not directly operate, update, or synchronize existing ML
repositories. It may read explicitly connected repositories for an approved
audit. Findings and proposals are written in Core; changes to an ML repository
are separate work owned by that repository.

## Candidate new-project skeleton

Bootstrap creates one universal foundation. It does not ask for or apply an
adapter.

```text
new-project/
|-- README.md
|-- AGENTS.md
|-- PROJECT_ROADMAP.md
|-- PROJECT_LOG.md
|-- .codex/
|   |-- config.toml
|   `-- agents/
|       |-- terra_worker.toml
|       |-- luna_clerk.toml
|       `-- sol_specialist.toml
|-- docs/
|-- tools/
|   `-- work_log.py
|-- tests/
`-- reports/
    |-- agent_tasks.jsonl
    `-- ml_work.jsonl
```

The empty `docs/` directory is part of the foundation. After the repository
audits, a small set of standard project documents may be proposed if repeated
real needs justify them.

## First manual adaptation

`README.md` is the first adaptation surface. The agent and human define:

- what the project is and why it exists;
- its current state and intended result;
- its main commands or entry points when known;
- where roadmap, logs, reports, and project documentation live.

Further project-specific rules are added manually inside the new repository.
Bootstrap does not choose a domain, generate an ML protocol, or install an
adapter overlay.

## Existing-project profiles

Core may keep short read-only profiles for explicitly connected projects:

```text
projects/
|-- generative_ml.md
`-- classical_ml.md
```

These are project profiles, not `.codex/agents` profiles and not templates.
They describe repository purpose, distinctive rules, human gates, important
files, and audit entry points. They do not control or mutate the project.

## Stable shared tools

One `work_log.py` lives in Core and is included in every new foundation. It
uses separate agent and ML subcommands and writes to separate journals. It
must remain small, domain-neutral, and stable enough that a normal project
does not need to fork it.

A project agent must not modify the tool without a concrete need and prior
human approval. If it is insufficient, the agent first reports the missing
capability. The preferred response is to improve the Core version deliberately
and use that lesson for future projects, not to create silent incompatible
variants.

The current large differences between `agent_ledger.py` and
`experiment_ledger.py` in the two ML repositories are historical evidence for
the audit. They do not need to be preserved in the future design.

## Difference detection

Automatic tracking and synchronization are deferred. Do not implement a
comparison script in the first Core simplification.

The approved order is:

1. simplify Core and make the minimal foundation reliable;
2. adapt the two existing ML repositories through separate work owned by each
   repository;
3. only then decide whether difference detection is still useful.

If it remains useful, the first version is a read-only comparison script over
one explicit file list. It reports:

- matching files;
- changed files;
- missing files;
- additional known orchestration files.

It never applies changes, updates a target repository, or treats every
difference as an error.

## Core's own foundation

Core uses the same minimal foundation that it generates for a new repository.
The default `tools/` and `tests/` directories exist even before the first tool
is implemented. Core also keeps additional files needed for its own purpose,
such as workbench notes, connected-project profiles, templates, implementation
tests, and Core development documentation. These additions do not create a
second agent system or a different set of universal rules.

Small Markdown reports and the universal `agent_tasks.jsonl` and
`ml_work.jsonl` journals are committed and pushed as normal repository
evidence. Secrets, private data, datasets, model artifacts, and large generated
outputs are excluded and referenced from reports when needed.

## Simplification rule

Core is experimental and may be simplified aggressively. Existing files,
schemas, locks, manifests, compatibility layers, and documentation are not
preserved merely because they already exist.

Before removal, determine whether a file supports a current accepted need.
When it does not, prefer deleting it and relying on Git history over keeping a
deprecated duplicate or compatibility path. Do not carry the current complex
ledger and adapter machinery into the new foundation without evidence from
the repository audits.

## Development gate

Do not implement this foundation until:

1. all current discussion decisions are saved in workbench candidates;
2. both connected ML repositories are audited read-only;
3. the candidates are checked against real agent histories and tool
   differences;
4. the final minimal file list and implementation task are approved.
