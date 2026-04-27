# Codex ResearchOS Runbook

This runbook tells Codex and human operators how to use this repository as a small research operating system.

## Start a new run

1. Define the research goal.
2. Identify pipeline and domain.
3. Create or update `state.json`.
4. Append a `decision` event to `events.jsonl`.
5. Execute only the smallest next useful action.
6. Write a report under `workspace/reports/`.

## Continue an existing run

Before executing, recover from:

- `state.json`
- `events.jsonl`
- `runs/last_run_id`
- `workspace/reports/`
- `workspace/runs/`
- `workspace/projects/`

Do not rely on chat memory.

## Event schema

Use JSON Lines.

```json
{"event_type":"decision","run_id":"run_YYYYMMDD_001","timestamp":"2026-04-27T00:00:00Z","summary":"Planned next action."}
```

Allowed event types:

- `decision`
- `model_call`
- `research_assessment`
- `execution`
- `review`

## Claim boundaries

Every research output must separate:

- supported claims
- partially supported claims
- unsupported claims
- next experiment needed

## Stop conditions

Stop and ask for human review when:

- the next command is high-risk
- evidence changes a core scientific claim
- inputs are missing
- results are unstable
- the repository structure would require a large redesign

## Smoke checks

```bash
python3 -m json.tool state.json
tail -n 5 events.jsonl
find workspace -maxdepth 3 -type f | sort | head -100
```
