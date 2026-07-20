# Candidate: simple ML work log

**Status:** discussion candidate only.
**Implementation authorization:** none.

## Purpose

Keep a short searchable history of meaningful ML work without duplicating
reports, metrics, configurations, or artifacts.

Each record should answer:

- when and what was done;
- the short result or stop reason;
- the decision, limitation, or next step;
- where the detailed report or artifacts can be found.

## Candidate workflow

After a meaningful ML run, evaluation, comparison, or investigation, the
worker invokes one simple script command. The worker supplies only a concise
summary and relevant repository-relative links. The script adds technical
fields such as record ID, UTC timestamp, repository, branch, and HEAD.

Illustrative interface:

```powershell
python tools/work_log.py ml add `
  --summary "Compared baseline and REPA under the approved quick protocol." `
  --result "Baseline was stronger on FID/KID; REPA improved from 10k to 20k." `
  --decision "Do not start a full evaluation yet." `
  --report "evaluation/baseline_vs_repa/report.md"
```

The exact command and field names are provisional. Normal use should require
one command and no schema reading or hand-written JSON.

## Where details belong

Detailed metrics, checkpoint hashes, dataset information, configurations,
tables, plots, commands, and long conclusions stay in project reports and
artifacts. The log contains only a short summary and links to those sources.

If details are needed later, search the journal, open the linked report, and
inspect the repository history.

## Relationship to adapters

The log format is shared across ML projects. Adapters define project-specific
rules, human gates, required checks, and report contents, but do not add
domain-specific fields to the journal.

Generative and classical ML therefore use the same short log even though their
reports and execution rules differ.

## Simplicity constraints

- One record per meaningful ML operation or coherent comparison.
- No mandatory start/review lifecycle.
- No fixed metric, model, checkpoint, dataset, or framework fields.
- No duplication of detailed reports.
- No token or cost accounting.
- No commit required for every record.
- Do not log routine file reads, test reruns, or minor implementation actions.

The storage format, minimum command interface, and exact definition of
"meaningful ML work" must be discussed before implementation.
