# Project-to-Manuscript Playbook

This playbook describes the v0.5 Project Orchestrator loop.

## Goal

Turn a project name and project description into a recoverable ResearchOS project, task graph, verification report, and evidence-gated manuscript draft.

```text
project name + project description
  -> quest
  -> task graph
  -> scheduler
  -> safe execution
  -> verification
  -> manuscript draft
```

## One-command local loop

```bash
python3 scripts/autonomous_project_loop.py \
  --project-name "My Project" \
  --project-description "Project description..." \
  --max-steps 8 \
  --autonomy POA2_execute_safe_local
```

## Expected outputs

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
workspace/reports/<project_id>_autonomous_project_loop_report.md
```

## Evidence-gated manuscript rule

The manuscript draft may describe artifacts that were actually created. It must not claim empirical superiority, target-journal readiness, broad generalization, p-values, citations, or experimental results unless those artifacts exist and are verified.

## Safe autonomy

Default autonomy is `POA2_execute_safe_local`. Long compute, network access, external data, wet-lab work, or journal submission require human approval.
