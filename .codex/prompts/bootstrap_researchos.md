# Codex Task: Bootstrap BearScientist / ResearchOS safely

You are configuring this repository as a BearScientist-style ResearchOS.

## Goal

Make the smallest useful PR that lets future Codex tasks recover state, choose the next research action, execute safely, and record claim boundaries.

## Hard constraints

- First inspect the repo; do not assume existing structure.
- Do not create a huge framework.
- Do not fabricate scientific results.
- Do not run long experiments.
- Do not store secrets or full prompts.
- Prefer one small PR over a broad rewrite.

## Step 1: Read-only recovery

Inspect:

- `README.md`
- `AGENTS.md`
- `runs/`
- `runs/last_run_id`
- `state.json`
- `events.jsonl`
- `workspace/reports/`
- `workspace/runs/`
- `workspace/projects/`
- existing tests / scripts

Then report:

- current repo state
- whether this is blank, partially bootstrapped, or active
- missing minimum ResearchOS files
- safest next PR

## Step 2: Minimal files to create if absent

Only create files that are immediately useful:

```text
state.json
events.jsonl
workspace/reports/README.md
workspace/runs/.gitkeep
workspace/projects/.gitkeep
docs/codex_researchos_runbook.md
```

## Step 3: Runbook content

`docs/codex_researchos_runbook.md` should explain:

- how to start a new research run
- how to recover from previous runs
- event types
- claim-boundary rules
- how to stop safely
- exact smoke-test commands

## Step 4: Verification

Run the smallest possible checks, for example:

```bash
find . -maxdepth 3 -type f | sort | head -100
python3 -m json.tool state.json
tail -n 5 events.jsonl
```

## Final response

End with:

- files changed
- commands run
- what is now configured for Codex
- what remains manual
- next recommended task
