# AGENTS.md Addendum: Project Orchestrator v0.5

This addendum extends BearScientist / ResearchOS with a project-intake-to-manuscript autonomous loop.

If this file conflicts with root `AGENTS.md`, `AGENTS.journal_review_addendum.md`, or `AGENTS.evidence_completion_addendum.md`, follow the stricter scientific-integrity and safety rule.

## Mission

Given only:

```text
project_name
project_description
```

the agent should create a recoverable research project, allocate tasks, execute safe tasks, verify results, complete evidence where possible, and produce a manuscript draft that is honest about evidence strength.

The agent is not a prose generator. It is a research project operator.

## Canonical loop

```text
intake -> quest -> task graph -> schedule -> execute -> verify
       -> evidence completion -> claim update -> manuscript draft
       -> re-review -> replan
```

## Autonomy levels

- `POA0_plan_only`: create project, task graph, and reports only
- `POA1_prepare_artifacts`: create project artifacts and manuscript skeletons, no code execution
- `POA2_execute_safe_local`: execute safe local deterministic tasks and small scripts
- `POA3_execute_bounded_research`: run bounded simulations, derivations, and evidence-completion tasks within budget
- `POA4_human_approved_long_run`: long compute, network, data downloads, external services, wet-lab, or submission actions require approval

Default: `POA2_execute_safe_local`.

## Required project artifacts

For every project, create:

```text
workspace/projects/<project_id>/
  quest.json
  project_brief.md
  task_graph.json
  task_backlog.md
  hypotheses.md
  experiments.md
  claim_evidence_map.md
  evidence_plan.md
  verification_report.md
  manuscript_outline.md
  manuscript_draft.md
  project_state.json

workspace/scheduler/scheduler_report.md
```

## Task graph requirements

Every task must include:

- task_id
- title
- task_type
- priority
- dependencies
- status
- risk_level
- autonomy_required
- auto_runnable
- expected_artifact
- done_criterion
- verification_check
- manuscript_implication

Task types:

- `project_setup`
- `hypothesis_generation`
- `baseline_definition`
- `evidence_completion`
- `claim_mapping`
- `verification`
- `manuscript_outline`
- `manuscript_draft`
- `red_team_review`
- `journal_review`

## Scheduling policy

Select the next task by:

1. dependency readiness
2. blocker / major evidence value
3. low risk before high risk
4. shortest safe action first
5. manuscript impact
6. evidence impact

Do not execute tasks with unmet dependencies. Do not execute high-risk tasks without approval.

## Execution policy

A task may auto-execute only if:

- dependencies are complete
- `auto_runnable = true`
- autonomy level is allowed
- risk is low or approved medium
- outputs are written under `workspace/`

If a task needs unavailable data, long compute, external APIs, or real experiments, create a blocking task and a human approval note.

## Verification policy

Every executed task must produce:

- artifact existence check
- claim impact check
- evidence level update
- failure or uncertainty note
- next action

Verification must not be optimistic. A generated file is not evidence unless it supports a claim.

## Manuscript writing policy

The manuscript draft must be evidence-gated.

Allowed:

- title
- abstract with cautious claims
- introduction/background
- methods describing actually performed steps
- results only from produced artifacts
- discussion with limitations
- future work
- data/code availability placeholders
- AI assistance disclosure placeholder if required

Forbidden:

- fabricated results
- fabricated citations
- fabricated p-values/effect sizes
- pretending planned tasks are completed
- claiming submission-readiness without journal gate
- hiding failed or inconclusive evidence

## Completion definition

A project-to-manuscript loop is complete only when:

- project artifacts exist
- task graph exists
- at least one safe task was executed or explicitly blocked
- verification report exists
- claim-evidence map exists
- manuscript draft exists
- unresolved blockers are listed
- next action is clear

## Required final response from Codex

When running a project-orchestration task, report:

- project_id
- project stage
- tasks generated
- tasks executed
- tasks blocked
- verification result
- claim/evidence changes
- manuscript files created
- remaining blockers
- commands run
- next recommended autonomous task
- next required human-approved task
