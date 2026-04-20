# Topic 1 Phase-2 Research Baseline Update

- Updated Topic 1 training to strengthen condition sensitivity and robustness interpretation:
  - stronger coherence / bandwidth / misalignment conditioning in forward path
  - stronger robust augmentation branch during training
  - larger default pilot and smoke settings (still sandbox-manageable)
- Added pilot-side aggregated outputs:
  - `outputs/topic1/pilot/ablation_summary.csv`
  - `outputs/topic1/pilot/aggregated_comparison.png` (text-plot fallback)
- Backend status in this run: **surrogate** (PyTorch backend was not detected at runtime).
- Trend strength improved relative to previous baseline:
  - unique pilot val_acc values: **7**
  - spread: **0.203125**
  - robust training mean accuracy > ideal in this sweep
  - aligned > misaligned, single-wavelength > multi-wavelength, high coherence > reduced coherence

## Recommended next experiment

Run the same pilot config with `backend: torch` in an environment with PyTorch available, then compare surrogate vs torch on the new ablation table and trend figure.
