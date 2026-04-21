# Topic 1 Latest Canonical Baseline (No-Torch Surrogate)

_Last updated: April 21, 2026 (UTC)._  
This is the authoritative Topic 1 baseline under current no-torch constraints.

## Canonical config
- `configs/topic1/pilot_surrogate_canonical.yaml`
- backend: `surrogate`
- compact CPU profile: `image_size=16`, `epochs=1`, `train_samples=48`, `val_samples=24`

## Canonical outputs
- `outputs/topic1/pilot/pilot_sweep.csv`
- `outputs/topic1/pilot/ablation_pairwise.csv`
- `outputs/topic1/pilot/ablation_summary.csv`
- `outputs/topic1/pilot/aggregated_comparison.png`
- `outputs/topic1/pilot/paper_ablation.svg`
- `outputs/topic1/pilot/phase_bits_probe/phase_bits_sweep.csv`
- `outputs/topic1/pilot/pilot_summary.md`

## Current canonical deltas
- robust vs ideal: `+0.036458`
- aligned vs misaligned: `+0.151042`
- single vs multi wavelength: `-0.005208` (multi is slightly better in this compact run)
- high vs reduced coherence: `+0.005208`

## Interpretation scope
This baseline is intended for trend interpretation only (not torch-level parity claims):
- robust vs ideal training
- aligned vs misaligned settings
- single vs multi wavelength
- high vs reduced coherence
- extra cheap axis: phase quantization bits
