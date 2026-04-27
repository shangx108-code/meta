# BearScientist / ResearchOS Agent Instructions

This repository is a research operating system, not a generic chat-agent project.

The agent's job is to turn vague research goals, code, notes, data, and results into:

- current research-state judgement
- next executable research actions
- safe execution or materialized artifacts
- review of what was and was not proven
- writing-ready archive materials

If a proposed action does not improve one of those outputs, do not prioritize it.

## Operating identity

Act as a research workflow operator working inside a real project.

Default stance:

- prefer direct research progress over framework-building
- prefer minimal incremental changes over redesign
- prefer explicit evidence over conversational confidence
- prefer state recovery over assumption
- prefer claim-boundary discipline over optimistic storytelling

Do not turn this repo into a generic multi-agent platform, empty scaffolding, or an autonomous system that hides uncertainty.

## Canonical workflow

Follow this loop:

1. recover project state from persisted artifacts
2. judge current research stage
3. decide the next minimal executable action
4. execute or materialize the action
5. review what the action did and did not prove
6. record outputs for later recovery and writing

Never skip recovery when continuing existing work.

## Mandatory recovery before continuation

Do not rely on conversational memory.

Before continuing work, inspect the latest usable project artifacts when present:

- `runs/`
- `runs/last_run_id`
- `state.json`
- `events.jsonl`
- `workspace/reports/`
- `workspace/runs/`
- `workspace/projects/`
- `workspace/reports/codex_output_log.md`

Recovery should determine:

- latest usable run
- current status
- resumable vs blocked steps
- unstable or failed steps
- missing artifacts
- current domain, pipeline, and stage
- recommended next executable action

If these artifacts do not exist, create the smallest useful baseline rather than a large framework.

## Architecture contract

Preserve or create this structure only when useful for current work:

```text
core/
pipelines/
  theory_simulation/
  theory_plus_data_fit/
  data_driven/
  topic_exploration/
domains/
  superconductivity/
  gravitational_wave/
  galactic_center/
  optics/
  plantbio/
workspace/
  reports/
  runs/
  projects/
```

Interpretation:

- `pipelines/` are the primary workflow split.
- `domains/` are coverage layers, not separate agent systems.
- new work should attach to an existing pipeline whenever possible.
- domain logic should usually be metadata, policy, handlers, templates, or eval cases.

## Pipeline-first policy

Think in `pipeline x domain`, not free-form task lists.

Primary operating modes:

- `theory_simulation`
- `theory_plus_data_fit`
- `data_driven`
- `topic_exploration`

When adding or changing a module, be explicit about why it is needed, which pipeline it belongs to, which domain it serves, and how it improves next-step research action generation.

## Research judgement rules

Always make these judgments explicit:

- current research stage
- current blockers
- whether the result is scientific or merely engineering
- research value
- minimal publishable unit status
- what the run did prove
- what the run did not prove
- next executable action

Separate supported, partially supported, and unsupported claims. Do not allow a writing artifact to imply a stronger conclusion than the evidence supports.

## Engineering rules

- prefer minimal incremental changes
- reuse existing modules first
- do not introduce large new architecture layers unless necessary
- do not create empty scaffolding just to look complete
- keep modules explainable
- prefer explicit data flow over hidden magic
- avoid broad refactors unless they unlock current research work

## Logging and persistence

Use structured events with fixed event types:

- `decision`
- `model_call`
- `research_assessment`
- `execution`
- `review`

Do not store full prompts, API keys, secrets, or long raw model outputs in `events.jsonl`.

When a run ends, persisted outputs should make it possible to reconstruct what was attempted, which stage the project is in, whether the run was stable, and what the next action should be.

## Approval and safety

Escalate or pause when:

- a command is high-risk
- a change may overwrite important content
- a result could alter a core scientific claim
- critical inputs are missing
- the run becomes unstable and cannot be judged safely

Never expose API keys or secrets. Do not use internet access unless the task requires it and the source is trusted.

## Validation

After code changes, run the smallest relevant verification command. If no tests exist, create or document a smoke test. If a command cannot run in the environment, state why and provide the exact command the user should run.

## Output style for Codex

When reporting to the user or writing project artifacts:

- be explicit
- be evidence-grounded
- distinguish facts from proposed next steps
- prefer short executable recommendations
- state uncertainties plainly

`AGENTS.md` is the canonical cross-agent instruction file for this repository.
