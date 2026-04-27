# Codex Task: Continue a ResearchOS run

Before doing any new work, recover state from persisted artifacts.

## Recovery checklist

Read, if present:

- `state.json`
- `events.jsonl`
- `runs/last_run_id`
- `workspace/reports/codex_output_log.md`
- latest files under `workspace/reports/`
- latest files under `workspace/runs/`
- relevant project files under `workspace/projects/`

## Required judgement

Report:

- latest usable run
- current domain
- current pipeline
- current stage
- whether the run is resumable or blocked
- next minimal executable action
- risk level: simple / medium / hard

## Execution rule

Execute only the smallest next action that improves research progress.

After execution, append a structured event and write/update a short report.

## Claim-boundary rule

Every report must distinguish:

- supported claims
- partially supported claims
- unsupported claims
- next experiment needed
