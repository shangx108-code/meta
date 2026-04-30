# Manuscript writing constraints and citation policy

## Figure policy

1. Figure 1 must be a conceptual schematic, mechanism diagram, or workflow figure.
   - It may be generated with GPT-images-2.0 or another illustration workflow.
   - It must be explicitly labeled as a schematic/conceptual figure.
   - It must not be presented as numerical data.

2. All remaining scientific/data figures must be generated from real project data.
   - No synthetic or illustrative data plots are allowed for Figs. 2 onward.
   - Each data panel must have a matching raw-data CSV/NPY/JSON file and plotting script.
   - Caption wording must state what quantity is computed and what parameter cut is used.

## Introduction structure

Use a classic four-paragraph introduction:

1. Broad motivation and field context
   - Majorana zero modes, topological superconductivity, and the need for field-free / low-stray-field platforms.

2. Current bottleneck and literature gap
   - Local zero-bias/near-zero features are not sufficient because trivial Andreev, impurity, and accidental states can mimic Majorana-like signatures.
   - Existing planar Josephson and altermagnetic Josephson proposals motivate the direction but do not fully solve false-positive exclusion.

3. Our concept and mechanism
   - Compensated magnetic texture / altermagnetic-like spin splitting plus superconducting phase bias drives a topological transition without net magnetization.
   - The transition is tracked using bulk gap closing/reopening and a Z2 invariant.

4. Main results and evidence chain
   - Bulk phase diagram, phase-driven gap closing/reopening, open-boundary spectra, end localization, negative controls, disorder stability, and nonlocal response proxy.
   - State the central claim conservatively: trivial near-zero mimics can occur, but they fail the combined evidence chain.

## Reference policy

- The main manuscript bibliography must contain more than 30 references.
- Every reference must be checked against DOI, journal, year, and title before final submission.
- References should be grouped into at least five categories:
  1. Foundational Majorana/topological superconductivity papers.
  2. Engineered Majorana platforms and planar Josephson junctions.
  3. Altermagnetism / compensated magnetic superconducting platforms.
  4. Nonlocal conductance, crossed Andreev reflection, and electron cotunneling diagnostics.
  5. Trivial Andreev-bound-state / disorder / false-positive literature.

## Competing-literature positioning

A 2026 npj Quantum Materials paper, "Topological altermagnetic Josephson junctions" by Yang, Sun, Xie, and Law, already proposes altermagnetic Josephson junctions as field-free Majorana platforms. Our manuscript must therefore not claim novelty merely from using altermagnets or zero net magnetization. The differentiating point must be the complete diagnostic pipeline:

- compensated magnetic texture,
- phase-controlled Z2 transition,
- explicit trivial-mimic negative controls,
- disorder ensemble stability,
- nonlocal EC/CAR response proxy,
- fully traceable raw data and plotting scripts.

## Caption and claim-control rules

Avoid unsafe wording:
- "Zero modes appear only in the topological phase."
- "A zero-bias peak proves Majorana modes."
- "The impurity response confirms topological protection" without ensemble evidence.

Preferred wording:
- "The phase-driven transition converts a trivial near-zero mimic into a spectrally purified topological end-mode pair."
- "The topological assignment relies on the joint evidence of Z2 inversion, gap reopening, spectral isolation, disorder persistence, and nonlocal response contrast."
- "Local impurities can sharpen trivial near-zero states, so the diagnostic must not rely on local spectra alone."

## Submission-readiness checklist

Before submission, verify that:

- Figure 1 is schematic/workflow only.
- Figures 2+ are plotted only from real data.
- Every figure has a raw-data file and plotting script.
- The Introduction follows the four-paragraph structure.
- Bibliography has >30 verified references.
- All claims map to figures, supplementary sections, or raw data.
- The competing 2026 TAJJ paper is cited accurately and positioned fairly.
- No citation placeholder remains in final manuscript.
