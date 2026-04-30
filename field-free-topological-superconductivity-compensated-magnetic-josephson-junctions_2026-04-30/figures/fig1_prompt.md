# Figure 1 schematic prompt

Status: conceptual schematic only. This prompt is for GPT-images-2.0 or an equivalent illustration workflow. It must not be used to generate data panels.

## Main prompt

Create a clean Nature Physics-style conceptual schematic for a theoretical condensed-matter physics paper. The figure should show a compensated-magnetic Josephson junction platform for field-free topological superconductivity. Use a horizontal planar Josephson junction geometry: two superconducting leads on the left and right with phases +phi/2 and -phi/2, separated by a central compensated magnetic weak link. The magnetic weak link should have two sublattices with opposite spin arrows, zero net magnetization, and momentum-dependent spin splitting illustrated by a small inset showing alternating red/blue spin-split bands in k-space. Do not draw a uniform ferromagnetic stray field. Add a phase-bias knob labelled phi that drives a transition from a trivial near-zero mimic to a topological purified end-mode pair. At the two ends of the weak link, draw localized Majorana-like end modes as soft glowing zero-energy markers only on the topological side. Include a diagnostic workflow strip underneath with five icons: bulk gap closing/reopening, Z2 invariant flip, open-boundary end localization, impurity/disorder negative control, and nonlocal EC/CAR response. Use minimal colors, high contrast, white background, thin vector-like lines, journal-quality labels, no photorealism, no 3D rendering.

## Required labels

- Compensated magnetic weak link
- Zero net magnetization
- Superconducting phase bias phi
- Bulk gap closing / reopening
- Z2 flip
- Trivial near-zero mimic
- Topological purified pair
- Nonlocal EC/CAR diagnostic

## Negative prompt / avoid

Avoid photorealistic laboratory equipment, microscope images, random noise texture, unlabelled decorative wave patterns, exaggerated glowing effects, ferromagnetic stray-field arrows, data heatmaps, numerical axes, or any element that could be mistaken for a measured data plot.

## Caption seed

Figure 1 | Concept and diagnostic workflow. A compensated magnetic Josephson junction combines zero-net-magnetization spin splitting with a superconducting phase bias. The phase bias drives a bulk gap closing and reopening accompanied by a Z2 invariant flip. Because trivial near-zero edge-like states can appear on the pre-transition side, the topological assignment is based on the combined evidence of bulk topology, spectral purification, end localization, negative controls, and nonlocal EC/CAR response rather than on local near-zero modes alone.

## Manuscript rule

Figure 1 is the only non-data figure. Figures 2 and onward must be generated from real project data with raw data files and plotting scripts.