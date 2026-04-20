# Topic 1 Phase-3 Torch Push Update

## What changed vs current PR #1 baseline

- Increased default Topic 1 pilot scale (`epochs=3`, `train_samples=256`, `val_samples=96`) while keeping sweep size fixed.
- Strengthened Topic 1 conditioning/robustness separation logic in training forward path.
- Added clearer pairwise ablation outputs:
  - `outputs/topic1/pilot/ablation_pairwise.csv`
  - `outputs/topic1/pilot/paper_ablation.svg`

## Backend status

- Attempted PyTorch backend detection in runtime.
- Current environment result: **PyTorch unavailable** (`ModuleNotFoundError`), so `backend=auto` used **surrogate** fallback.

## Trend separation status

- Topic 1 pilot now shows 11 unique accuracy values with spread 0.3125 (from 0.104167 to 0.416667).
- Pairwise ablation now explicitly reports deltas for:
  - robust vs ideal
  - aligned vs misaligned
  - single wavelength vs multi-wavelength
  - high vs reduced coherence

## Recommended next experiment

Run the same pilot config in a PyTorch-enabled environment with `backend=torch`, then compare `ablation_pairwise.csv` and `paper_ablation.svg` across surrogate and torch backends.
