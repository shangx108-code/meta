# A | Compensated-Magnetic Josephson-Junction Blueprint

## Source lock
- Primary intake files: `/workspace/user_files/01-1-.txt` and `/workspace/user_files/02-2-.txt`
- Intake date: 2026-05-01
- Role of this note: freeze the compensated-magnetic Josephson-junction application branch as a reusable project object inside the long-term space

## Locked project interpretation
This branch is not "another Majorana platform" paper. The application is a compensated-magnetic or odd-parity-magnetic Josephson junction used to demonstrate a stronger claim: field-free, phase-controlled topological superconductivity together with a nonlocal diagnostic that excludes trivial near-zero mimics.

## Working title candidates
- Field-free topological superconductivity in compensated-magnetic Josephson junctions
- Field-free topological superconductivity and nonlocal Majorana fingerprints in compensated-magnetic Josephson junctions

## Central physics question
Can a compensated-magnetic Josephson junction realize a phase-controlled topological transition without net magnetization, and can that same platform support a transport-side discriminator that separates true Majorana end modes from trivial ABS-, impurity-, and disorder-induced near-zero states?

## Minimal model to keep fixed
- Geometry: planar Josephson junction with `S_L - CM - S_R`
- Pairing phases: `Delta_L = Delta exp(+i phi / 2)` and `Delta_R = Delta exp(-i phi / 2)`
- Normal-state lattice model:
  - `xi_k = -2 t (cos k_x + cos k_y) - mu`
  - Rashba term `alpha_R (sin k_y sigma_x - sin k_x sigma_y)`
  - compensated magnetic term `M(k) sigma_z` with `M(k) = M_0 (cos k_x - cos k_y)`
- Constraint that must stay explicit: `B_Z = 0`

## Core claim stack for this branch
1. The compensated magnetic texture plus phase bias can drive a bulk topological transition without net magnetization.
2. Open-boundary near-zero end modes exist, but local near-zero structure alone is not a sufficient topological proof.
3. Nonlocal conductance and CAR/EC structure change with the same phase window as the bulk transition.
4. Trivial controls can fake local peaks but fail the combined bulk-plus-nonlocal consistency test.

## Required negative controls
- Control A: localized ABS from a Gaussian end potential
- Control B: YSR-like impurity state from a magnetic impurity treated in a T-matrix language
- Control C: disorder-induced near-zero states from a random on-site potential ensemble

## Main-text figure skeleton
- Figure 1: concept and mechanism schematic only
- Figure 2: bulk topology maps versus `phi`, `mu`, and `M_0`, with gap-closing lines
- Figure 3: open-boundary spectra, end localization, and Majorana self-conjugacy diagnostics
- Figure 4: `G_LL`, `G_RR`, `G_LR`, and `CAR - EC` versus `V` and `phi`
- Figure 5: true Majorana versus ABS/YSR/disorder comparison table or diagnostic panel

## Why this branch is still viable after TAJJ
- The novelty cannot rest on "altermagnetic Josephson junctions host topology."
- The viable claim is the combination of:
  - compensated-magnetic field-free application,
  - phase-controlled topology,
  - explicit false-positive exclusion,
  - experimentally legible nonlocal transport protocol.

## Immediate execution implication
The next numerical package for this branch must produce real source-data panels for bulk topology, open-boundary spectra, nonlocal transport, and negative controls in one auditable folder. No prose-only upgrade is sufficient.
