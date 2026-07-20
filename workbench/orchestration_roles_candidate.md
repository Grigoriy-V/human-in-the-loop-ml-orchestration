# Candidate: human, supervisor, and worker operating model

**Status:** discussion candidate only.
**Implementation authorization:** none.
**Purpose:** preserve the complete working context needed to later simplify
`AGENTS.md`, agent profiles, task specifications, and orchestration rules.

This document describes the intended operating relationship. It is not yet an
active instruction and does not authorize code, test, evaluation, training, or
tool changes.

## Problem being addressed

The orchestration system drifted from a previously successful pattern:

- a Sol conversation handled learning, strategy, and task design;
- a Terra conversation performed the implementation, testing, evaluation, and
  other hands-on work;
- the human chose when discussion was mature enough to become an execution
  task and manually transferred the resulting specification to Terra.

After more lifecycle, logging, validation, and delegation rules were added,
routine work began to fragment into repeated supervisor/worker handoffs. The
supervisor sometimes performed more calls and consumed more attention than the
worker. A recent observed usage snapshot showed Sol `86`, Terra `19`, Luna `6`,
and auto-review `4`. The numbers do not by themselves prove token cost, but
they show the routing imbalance that this candidate is meant to correct.

The target is not unrestricted worker autonomy. The target is clear ownership:

- the human controls direction and the transition from discussion to work;
- the supervisor owns interpretation, strategy, delegation, and acceptance;
- the worker owns the complete execution loop inside the approved result and
  boundaries.

## Historical working reference

A successful generative-ML task used the following pattern.

The Sol-created specification defined:

- the end result: one comparison pipeline and one command;
- fixed checkpoints and a matched evaluation protocol;
- invariants such as seeds, sample budget, metrics, hashes, and artifact
  immutability;
- forbidden expansion: no new training, full-1000, sampler ablation, or CFG
  sweep;
- required outputs: implementation, tests, metrics, visual artifacts,
  documentation, ledger evidence, and a commit;
- acceptance evidence and the contents of the final report.

Terra then independently:

- found and verified checkpoint paths and hashes;
- designed and implemented the reusable CLI and configuration;
- wrote and ran tests;
- diagnosed and fixed problems;
- ran the approved quick evaluation;
- produced metrics, grids, manifests, reports, and documentation;
- updated the relevant evidence;
- committed the accepted work;
- returned once with the command, `40 passed`, metrics, hashes, performance,
  artifacts, limitations, and commit.

The important instruction was effectively:

> If the pipeline fails, fix it and repeat the approved quick-200 evaluation.
> Do not expand to full-1000.

This granted autonomy for diagnosis and retry while preserving a clear cost
and scope boundary.

## Human role: client and learning partner

The human is not expected to arrive with a complete technical specification.
The human may:

- explore a topic and learn how it works;
- ask strategic and technical questions;
- compare options;
- change or refine the desired outcome during discussion;
- decide when discussion is mature enough to become work;
- make product, strategy, budget, and human-gated decisions.

The human is not required to:

- write the worker task specification;
- choose the worker profile;
- enumerate files or commands;
- manually transfer a specification between chats;
- operate agent lifecycle or logging machinery;
- know the implementation details needed to make the task executable.

The interaction is similar to a client working with a responsible technical
supervisor. If the request is incomplete or uncertain, the supervisor helps
turn it into a coherent direction instead of treating the user's wording as a
complete implementation contract.

## Supervisor accountability

The Sol-based main conversation is the supervisor.

The supervisor owns:

- discussion and explanation;
- reconstruction of current project state;
- distinction between ideas, candidates, decisions, and approved work;
- strategic choices and roadmap interpretation;
- selection of the next useful task;
- worker/profile selection;
- task specification quality;
- coordination and scope boundaries;
- review of the worker's actual diff, tests, evidence, and limitations;
- the final accept, rework, stop, or defer decision;
- the concise report returned to the human.

The supervisor is accountable when:

- the worker receives an unclear, contradictory, or unnecessarily narrow task;
- the wrong worker/profile is selected;
- a normal task is fragmented into avoidable micro-tasks;
- routine implementation decisions are repeatedly escalated;
- the work crosses a boundary that the supervisor should have stated;
- the worker's evidence is accepted without adequate review.

Worker defects can still occur, and external systems can fail. Supervisor
accountability means diagnosing and correcting the orchestration rather than
blaming the human for not having supplied an implementation-ready request.

## Discussion and execution modes

### Discussion mode

Discussion is the default while the human and supervisor are:

- learning;
- exploring alternatives;
- defining the real problem;
- comparing trade-offs;
- recording candidates;
- deciding what is worth doing.

Discussion does not automatically authorize implementation or worker
dispatch. The supervisor may perform relevant read-only inspection and, when
explicitly allowed, a small direct documentation action.

### Execution mode

Execution begins after an unambiguous human command such as:

- "start work";
- "continue work";
- "follow the plan";
- another clear instruction to execute the agreed direction.

The human no longer needs to request a separate specification and manually
copy it to Terra. The supervisor converts the accepted discussion into a
bounded task and dispatches the appropriate worker.

Suggested command semantics:

- **Start work:** formulate and dispatch the agreed next task.
- **Continue work:** restore and continue the current approved task without
  opening a new strategic direction.
- **Follow the plan:** select the next accepted and incomplete roadmap item and
  organize its execution.

These commands operate within existing human gates. If the next action needs
new external authority, meaningful strategy choice, destructive action,
publication, or a separately gated expensive run, the supervisor asks once
for that decision.

## Sol-supervisor direct work

The supervisor may directly:

- read project rules, roadmap, reports, logs, and Git state;
- explain or compare options;
- inspect a worker's result;
- make one small, coherent documentation or roadmap change;
- record a discussion candidate or short decision when explicitly authorized.

A direct write is appropriate when all of the following are true:

- no implementation code is involved;
- no test, benchmark, evaluation, or training is required;
- the change is one coherent action;
- it is confined to a small documentation surface;
- no prolonged diagnosis is required;
- delegating and logging a worker would clearly cost more than the action.

The supervisor must not turn direct permission into a long implementation
session. If the work grows beyond a small coherent action, the supervisor
dispatches the remaining complete task once rather than continuing through
many expensive tool iterations.

## Terra worker role

Terra is the default hands-on implementation and validation worker.

Terra may perform, when required by the assigned result:

- repository and code inspection;
- implementation and refactoring;
- configuration changes;
- focused and full tests appropriate to the change;
- debugging and correction of its own work;
- approved benchmarks and evaluations;
- approved data or ML operations within explicit gates;
- related technical documentation and evidence updates;
- preparation of exact commands for human-gated operations;
- Git operations explicitly included in the task.

Terra does not choose a new project direction or silently expand the experiment
or product scope. It owns the method of achieving the assigned result.

## Worker autonomy

The supervisor assigns an outcome, repository, invariants, forbidden
boundaries, acceptance criteria, and human gates. The supervisor should not
enumerate every permitted command or predict every file that may be needed.

After dispatch, the worker independently:

1. inspects the evidence and code needed for the task;
2. selects an implementation within the accepted direction;
3. changes the necessary in-scope files;
4. runs proportional tests and checks;
5. diagnoses failures caused or exposed by the work;
6. fixes and retries within the approved cost/protocol boundary;
7. updates required technical evidence;
8. creates one final task-log record under the separately discussed simplified
   logging candidate;
9. returns one consolidated report to the supervisor.

Routine implementation choices do not require new supervisor approval.
Ordinary test failures, local debugging, and correction of the worker's own
implementation are part of the same worker task, not new tasks.

The worker should not return after every intermediate error. If blocked, it
returns one consolidated report containing:

- the intended result;
- what was tried;
- the exact blocker;
- what was ruled out;
- the recommended next decision;
- the specific authority or information required.

If the supervisor requests rework, it should send the same worker one
consolidated set of findings whenever practical. A new worker, reviewer, or
task chain is not created for each minor correction.

## Worker stop conditions

The worker stops and returns control when:

- a human approval gate is reached;
- a destructive, externally mutating, publishing, or materially expensive
  action is not already authorized;
- completing the result requires a strategic or roadmap change;
- the work must leave the assigned repository or materially expand scope;
- credentials, secrets, or unavailable external information are required;
- unrelated user changes or writer conflicts make safe continuation uncertain;
- repeated diagnostic attempts produce no new evidence and the same blocker
  remains.

These are boundary stops, not routine debugging stops.

A logging-tool failure should not erase or invalidate completed primary work.
The worker reports the logging failure with its normal result instead of
starting a separate repair chain unless the logging tool itself was the
assigned task.

## Luna clerk role

Luna is used for bounded, substantial clerical work that is cheaper to
delegate than to perform in the Sol conversation, including:

- multi-file extraction and inventory;
- normalization or formatting;
- deterministic collection of statuses or evidence;
- execution of existing safe scripts that require no implementation judgment;
- preparation of a factual summary.

Luna does not:

- make strategy or project decisions;
- implement or debug code;
- design experiments;
- interpret ambiguous results;
- receive a one-line task when delegation overhead is greater than direct Sol
  execution.

Within a suitable clerical task, Luna should also work autonomously and return
one result rather than creating repeated micro-handoffs.

## Specialist and independent review

A separate specialist worker is not the normal Sol-supervisor.
Independent specialist review is reserved for explicitly justified cases such
as:

- security or privacy;
- publication or externally visible release;
- destructive or high-risk migration;
- changes to the logging, validation, or governance system itself;
- a complex blocker that Terra cannot resolve within the approved task.

Routine implementation does not automatically require a separate reviewer.
The supervisor reviews the worker result.

## Task specification structure

A worker task should describe the result and boundaries rather than a
step-by-step shell script.

For a substantial task, the useful sections are:

1. **Goal:** the observable result to deliver.
2. **Current state:** evidence and assumptions already known.
3. **Invariants/protocol:** facts and procedures that must remain fixed.
4. **Forbidden actions and gates:** what must not happen without approval.
5. **Acceptance criteria:** evidence required to call the task complete.
6. **Final report:** what the worker must return.

The specification may include exact paths, commands, protocols, or artifacts
when they are genuinely fixed. It should otherwise allow the worker to select
necessary files and commands inside the task.

Specification detail should be proportional to execution cost and risk. A
large ML comparison can justify a detailed protocol. A one-file roadmap note
cannot justify a comparable task contract.

## Normal end-to-end flow

```text
Human and Sol discuss and learn
-> human commands start/continue/follow the plan
-> Sol chooses the next result and writes one bounded specification
-> Terra or Luna owns the complete execution loop
-> worker returns one task record and consolidated evidence
-> Sol reviews the actual result once
-> Sol accepts or sends one consolidated rework request
-> Sol reports the outcome to the human
```

The intended balance is that Sol spends effort on understanding, strategy,
specification, and acceptance, while Terra performs the longer implementation
and validation work. Repeated supervisor/worker handoffs per completed task are
a warning signal.

## Candidate core principles

1. The human controls direction and the transition from discussion to work.
2. The supervisor owns interpretation, task design, routing, and acceptance.
3. The worker owns implementation method and the internal fix/test/retry loop.
4. Delegation is used when it separates strategy from execution or saves work.
5. Sol performs small coherent documentation actions directly when delegation
   would cost more.
6. Terra handles code, tests, evaluation, and other hands-on engineering.
7. Luna handles substantial deterministic clerical work, not trivial writes.
8. Workers return complete results or one consolidated blocker, not a stream of
   routine approval requests.
9. Human gates protect meaningful cost, authority, privacy, and external
   effects; they do not micromanage normal implementation.
10. Logging and review must not become more expensive than the task.

## Questions before turning this into instructions

1. How to define "small coherent direct action" without a rigid line or tool
   count that creates new edge cases.
2. Which evaluations and benchmarks Terra may run directly when explicitly
   included in the task, and which remain separately human-gated.
3. How to distinguish a reasonable internal retry loop from a worker spending
   too long without progress.
4. What minimum evidence the supervisor needs for acceptance in routine,
   implementation, and ML tasks.
5. Which rule text belongs in the short root `AGENTS.md` and which detail, if
   any, remains in profile-specific instructions.
6. How to measure Sol/Terra work balance and handoff overhead without adding
   intrusive tracking.

These questions should be discussed before editing the active orchestration
policy.

## Related candidate

See `workbench/agent_task_log_candidate.md` for the separately discussed
single-record worker logging proposal. The future logging design should support
this operating model rather than dictate it.
