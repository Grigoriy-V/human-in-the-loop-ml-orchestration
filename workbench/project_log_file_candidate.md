# Candidate: PROJECT_LOG.md

**Status:** discussion draft only.
**Implementation authorization:** none.

This file demonstrates a compact, agent-maintained project history. It is not
an agent task ledger and not a detailed ML experiment report.

---

# Project Log

This log records important completed milestones, investigations, and project
decisions. It is maintained by the agent that completes the work. Detailed
commands, metrics, artifacts, and raw output stay in linked reports and work
journals.

## How to maintain this file

- Add an entry after an important project result, decision, or closed roadmap
  step, not after every implementation action or test rerun.
- Keep one `# Project Log` heading. Add new dated entries to the same document.
- Use a short title that makes the history searchable by scanning headings.
- Summarize the outcome and decision; link to detailed evidence when it exists.
- State an important limitation or stop reason instead of hiding it.
- Do not copy raw command output, full metric tables, or agent lifecycle data.
- Do not use a log tool for this Markdown file; the responsible agent edits it
  directly and follows this embedded format.

To reconstruct history, scan dated headings first and read only the relevant
entries and linked reports.

## Entry shape

```markdown
## YYYY-MM-DD: Short milestone name

### Goal

Why this work was done. Omit this section when the title and context are
already sufficient.

### Outcome

What materially happened, including a short result and links to evidence.

### Decision

What was accepted, stopped, deferred, or selected. Include the important
limitation or next boundary when relevant.
```

`Goal` is optional. `Outcome` and `Decision` are the normal minimum. Evidence
links may be included inside either section instead of requiring a separate
field.

## Example

## 2026-07-20: Minimal agent logging candidate

### Goal

Replace a failure-prone multi-event lifecycle with one simple worker-owned
task record.

### Outcome

Prepared a candidate interface in
`workbench/agent_task_log_candidate.md`. No active rules or tools changed.

### Decision

Keep one final task record per worker attempt. Do not implement until the two
ML repositories have been audited against the candidate.

## Relationship to other files

- `PROJECT_ROADMAP.md` contains current direction, the approved step, and later
  ideas.
- `PROJECT_LOG.md` contains the short human-readable history of important
  completed work and decisions.
- The agent task log contains individual worker outcomes.
- The ML work log indexes meaningful ML operations and detailed reports.
- Reports contain commands, metrics, analysis, and artifacts that would make
  this file too large.
