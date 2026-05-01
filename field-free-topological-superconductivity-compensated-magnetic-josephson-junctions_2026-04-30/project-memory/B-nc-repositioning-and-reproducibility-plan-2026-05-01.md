# B | Nature Communications Repositioning And Reproducibility Plan

## Source lock
- Primary intake file: `/workspace/user_files/03-markdown-1-md-9`
- Intake date: 2026-05-01
- Role of this note: freeze the Nature Communications packaging path as the fallback-to-advance venue plan for the same project

## Locked venue judgment
- Nature Physics remains the high bar, but the present evidence chain is not there yet.
- Nature Communications is a live and realistic target if the claims are tightened and the reproducibility package becomes complete.

## Locked NC title
False-positive-resistant nonlocal diagnosis of field-free topological superconductivity in compensated-magnetic Josephson junctions

## Locked NC central sentence
We are not selling another compensated-magnetic Josephson platform. We are establishing a false-positive-resistant, phase-resolved nonlocal diagnostic protocol that separates true topological end modes from impurity-, ABS-, and disorder-induced near-zero mimics in a field-free superconducting device.

## Five main-text claims to keep
1. Compensated magnetism plus phase bias produces a bulk topological transition with gap closing/reopening and `Z2` change.
2. Open-boundary near-zero modes exist, but local spectrum alone does not diagnose topology.
3. Impurity and disorder controls can generate false local near-zero features.
4. Phase-resolved nonlocal response is stricter than local spectroscopy.
5. The combined diagnostic remains stable under finite perturbations, temperature broadening, and disorder statistics.

## Locked five-figure main-text structure
- Figure 1: concept plus false-positive problem
- Figure 2: bulk topology map
- Figure 3: boundary spectra and local ambiguity
- Figure 4: negative controls
- Figure 5: lead-resolved nonlocal transport criterion

## Required package upgrades before NC is credible
- Source data for every panel in Figures 2-5
- Plotting scripts for every panel in Figures 2-5
- Config files with complete parameters and seeds
- Supplement sections covering model, invariant, open-boundary numerics, disorder controls, lead-attached transport, effective model, and reproducibility
- Data Availability statement
- Code Availability statement
- Prior-art table that explicitly separates this paper from Yang 2026 TAJJ

## Locked writing constraints
- Do not use "universal", "near-optimal", "model-agnostic", or "complete closure" in the abstract.
- Do not claim that a local zero-bias peak proves a Majorana mode.
- Do not sell the paper as the first altermagnetic or compensated-magnetic Josephson platform.
- Keep the novelty anchored in the diagnostic protocol and false-positive exclusion.

## Minimal repo/package layout that the manuscript should converge to
```text
cmjj-nonlocal-diagnostic/
  README.md
  environment.yml
  CITATION.cff
  configs/
  data/source_data_fig2/
  data/source_data_fig3/
  data/source_data_fig4/
  data/source_data_fig5/
  scripts/
  manuscript/main.tex
  manuscript/supplement.tex
```

## Immediate execution implication
The shortest path is not more theory prose. It is one auditable figure-and-data sprint that turns the compensated-magnetic application into a reproducible Figures 2-5 package with source data, scripts, and a prior-art comparison table.
