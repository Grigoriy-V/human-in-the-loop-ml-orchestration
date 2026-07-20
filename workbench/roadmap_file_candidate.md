# Candidate: project roadmap

**Status:** discussion draft only.
**Implementation authorization:** none.

This file demonstrates a compact roadmap structure and its maintenance rules.
It is a candidate for adaptation, not an active project plan.

---

# Project Roadmap

**Updated:** YYYY-MM-DD

**Project status:** active / paused / blocked / completed

**Current approved step:** `2.1 Short step name` or `none`

This file is the single source of the project's accepted direction, current
state, next approved step, and later ideas. Detailed implementation tasks,
command output, metrics, and investigation notes stay in reports and work
logs.

## Operating rules

1. The supervisor reads this roadmap before selecting or changing project
   work.
2. Work proceeds through one approved roadmap step at a time.
3. The supervisor may turn the current approved step into a bounded worker
   task after the human says "start work", "continue work", or "follow the
   plan".
4. A general command to continue does not bypass an explicit human gate for a
   long, expensive, destructive, external, or otherwise consequential action.
5. An agent does not silently skip, merge, expand, reorder, or invent roadmap
   steps.
6. Discussion and backlog entries do not authorize execution.
7. A roadmap step may contain an autonomous implementation and retry loop, but
   moving to another roadmap step requires supervisor acceptance and the next
   human-approved transition.
8. The roadmap records concise state and decisions. Raw logs and detailed
   results remain in linked reports, artifacts, and work journals.

Project adapters may add domain-specific gates, checks, and evidence
requirements. They do not create a second roadmap or weaken these transition
rules.

## Current state

Summarize only what a new supervisor needs to understand the project now:

- what is already usable;
- what is paused, blocked, or intentionally excluded;
- the most important current limitation or decision;
- the current approved step, if one exists.

## Current approved step

### 2.1 Short step name - approved

**Goal:** one sentence describing the intended result.

**Why now:** one sentence connecting it to the current project state.

**Scope:** the bounded outcome, not a full worker task specification.

**Acceptance:** the evidence needed for the supervisor to accept the step.

**Gate:** `none`, or the exact action that still requires human approval.

Only one section may be marked as the current approved step. Detailed files,
commands, retry rules, and reporting requirements belong in the worker task
specification created when execution begins.

## Completed steps

Keep a short durable record for each accepted, stopped, or deliberately closed
step.

### 1.1 Example completed step - completed

- **Result:** implemented and verified the minimal comparison workflow.
- **Evidence:** `reports/example_comparison/report.md`.
- **Decision:** keep the workflow and use it for the next approved comparison.
- **Limitation:** only the quick protocol was run; full evaluation was not
  authorized.

Do not copy raw commands, full metric tables, or long reports into the roadmap.
Link to the source that contains them.

## Next candidates

These steps have been discussed but are not authorized merely because they are
listed.

1. `3.1 Candidate A` - short purpose and dependency.
2. `3.2 Candidate B` - short purpose and dependency.

When the human approves a candidate as the next step, move it to
`Current approved step` and update the header. Do not start it in the same
transition unless the human also authorizes execution.

## Later ideas

Store useful future directions here without presenting them as commitments.
Each idea needs only a short purpose. Research detail belongs in a separate
workbench note if it becomes necessary.

- **Idea:** what might be useful and why.

## How to maintain this file

After a material project decision, change only what the decision affects:

1. the project status or current approved step;
2. the factual result and link to evidence;
3. the accepted decision and known limitation;
4. the next candidate or transition approved by the human.

When a step completes, stops, or is deliberately closed:

1. move its concise outcome to `Completed steps`;
2. record result, evidence, decision, and limitation;
3. clear the current approved step;
4. discuss the next transition before approving another step.

When work is blocked or paused, record the reason and the condition for
resuming. When a new idea appears, add it to `Later ideas`; do not silently
insert it into active work.

The roadmap itself carries these maintenance instructions. No log tool is
required to edit a normal Markdown roadmap. A tool is useful only for
append-only machine-readable journals where direct agent editing would be
fragile.
