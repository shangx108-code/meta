# Topic 1 Design Rules (Surrogate No-Torch Baseline)

Derived from `outputs/topic1/pilot/ablation_pairwise.csv` and `outputs/topic1/pilot/phase_bits_probe/phase_bits_sweep.csv`.

## Key pairwise deltas
- ideal_vs_robust: Δ=`+0.036458` (robust - ideal)
- aligned_vs_misaligned: Δ=`+0.151042` (aligned - misaligned)
- single_vs_multi_wavelength: Δ=`-0.005208` (single - multi)
- high_vs_reduced_coherence: Δ=`+0.005208` (high - reduced)

## Practical conclusions
- **Robust training is worth the efficiency cost when shift/noise risk is real.**  
  In this compact pilot, robust improves mean accuracy by `+0.036458`.
- **Misalignment is the dominant failure mode.**  
  The alignment delta (`+0.151042`) is much larger than coherence and wavelength-count deltas.
- **Single wavelength is not clearly superior in this canonical compact run.**  
  Multi-wavelength is slightly better on average (`0.005208` absolute edge), so wavelength choice should be tuned jointly with robustness and alignment.
- **Coherence still matters, but less than alignment.**  
  High coherence gives a small gain (`+0.005208`) versus reduced coherence.
- **Phase quantization guidance:** 4-bit showed clear degradation; 6-8 bit tied in this run.

## What should wait for torch-backed implementation
- Any strong claim about architecture scaling (depth/width) or optimizer behavior.
- Final accuracy claims intended for publication tables.
- Surrogate-vs-physics parity validation on identical grids.
