# Topic 1 Design Rules (Surrogate No-Torch Baseline)

## Key pairwise deltas
- ideal_vs_robust: Δ=0.052734 (robust vs ideal)
- aligned_vs_misaligned: Δ=0.201172 (shift=0.0 vs shift=1.0)
- single_vs_multi_wavelength: Δ=0.025391 (num_wavelengths=1 vs num_wavelengths=3)
- high_vs_reduced_coherence: Δ=0.013672 (coherence=1.0 vs coherence=0.6)

## Practical conclusions
- **Robust training worth it** when misalignment risk exists: robust-vs-ideal delta=0.052734.
- **Single wavelength preferred** for current surrogate baseline when maximizing average accuracy: delta=0.025391.
- **Misalignment dominates operating regime**: aligned-vs-misaligned delta=0.201172.
- **Coherence effects are weaker than misalignment** in this baseline: coherence delta=0.013672 vs misalignment delta=0.201172.
- **Phase quantization guidance**: in probe sweep, best bits=6 with val_acc=0.171875.

## Scope note
These are surrogate-backend design rules for pre-torch iteration and should be re-validated once torch path is available.
