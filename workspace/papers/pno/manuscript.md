# Reconfigurable Photonic Neural Operators for Scientific PDE Solvers (Simulation Study)

## Abstract
We study reconfigurable photonic neural operators over Poisson/Helmholtz families with grid and parameter transfer. On unseen condition (grid=32, k=10), best model is fourier for Poisson (L2=0.4050) and local for Helmholtz (L2=0.4238).

## 1. Introduction
This manuscript targets simulation-first photonic computing design laws rather than single benchmark wins.

## 2. Methods
Finite-difference solvers are used as reference truth; three branches (fourier/local/hybrid) are compared across 2 PDEs × 2 grids × 2 k values.

## 3. Results
24 evaluation points show branch preference changes by PDE family, supporting the need for configurable operators and phase-diagram style reporting.

## 4. Claim boundaries
- Supported claims are restricted to the reported simulation setup.
- Hardware/deployment/SOTA claims are not made.

## 5. Reproducibility
- Script: `project_pno/scripts/run_phase2.py`
- Data artifact: `project_pno/results/phase2/phase2_generalization.csv`
- Assessment: `project_pno/results/phase2/phase2_assessment.json`
