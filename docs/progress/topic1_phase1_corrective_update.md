# Topic 1 Phase-1 Corrective Update

- Added backend selection (`auto`/`torch`/`surrogate`) in Topic 1 training.
- Implemented optional tensorized PyTorch path (used automatically when available).
- Strengthened surrogate path with trainable detector and perturbation-aware robust augmentation.
- Pilot sweep now has **3** unique validation accuracies: [0.21875, 0.34375, 0.375].
- Added robustness trend artifact at `outputs/topic1/pilot/robustness_trends.png`.
