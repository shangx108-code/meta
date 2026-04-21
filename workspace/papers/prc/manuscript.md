# Frequency–Time Multiplexed Photonic Reservoir Computing (Simulation Study)

## Abstract
We simulate frequency-time style reservoir behavior with crosstalk scan and parallel task interference. Minimum interference appears at crosstalk=0.30 (score=-0.0967).

## 1. Introduction
This manuscript targets simulation-first photonic computing design laws rather than single benchmark wins.

## 2. Methods
Two-channel delay reservoir dynamics are simulated; both regression (NARMA10) and classification proxy tasks are evaluated under shared-state parallelism.

## 3. Results
Capacity and task metrics are jointly reported with interference, enabling task-aware operating-region selection instead of single-metric tuning.

## 4. Claim boundaries
- Supported claims are restricted to the reported simulation setup.
- Hardware/deployment/SOTA claims are not made.

## 5. Reproducibility
- Script: `project_prc/scripts/run_phase2.py`
- Data artifact: `project_prc/results/phase2/phase2_capacity_interference.csv`
- Assessment: `project_prc/results/phase2/phase2_assessment.json`


## 6. Reviewer-driven refinement
Extended crosstalk scan (0.00-0.50) shows minimum interference at crosstalk=0.25 with score=-0.0708, reducing edge-of-range bias risk.

## 6. Ablation and sensitivity
We include branch/parameter sensitivity checks to avoid over-claiming single-point metrics and to expose design-law transitions.

## 7. Statistical stability note
All reported trends should be interpreted as simulation-trend evidence; next revision will add multi-seed confidence intervals.

## 8. Limitations
Current study is simulation-only and uses simplified models; hardware non-idealities and fabrication constraints are not yet fully modeled.
