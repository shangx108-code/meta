# Optical Neural Network Research Simulation Platform

Simulation-first research codebase for three topics:
1. **Topic 1**: Broadband and partially-coherent robust diffractive optical neural networks under fabrication/alignment errors.
2. **Topic 2**: Device-aware nonlinear activation co-design for scalable optical neural networks.
3. **Topic 4**: Multiplexed multi-task optical neural networks via wavelength/polarization/spatial-mode DoFs.

## Quick start (cross-platform)

```bash
python -m src.training.train_topic1 --config configs/topic1/smoke.yaml
python -m src.experiments.topic1_pilot --config configs/topic1/pilot.yaml
python -m src.experiments.topic2_smoke --config configs/topic2/smoke.yaml
python -m src.experiments.topic4_smoke --config configs/topic4/smoke.yaml
```

Shell wrappers remain available under `scripts/` for CI/sandbox use.

## Topic 1 backend policy

- `backend: auto` (default): use PyTorch tensorized path if available; otherwise use surrogate fallback.
- `backend: torch`: require PyTorch, fail fast if unavailable.
- `backend: surrogate`: always use lightweight fallback.

## Structure

- `configs/`: configs for each topic.
- `src/core`: propagation, coherence, wavelength sampling, noise, and metrics.
- `src/models`: D2NN, nonlinear activations, multiplexing modules.
- `src/training`: training losses and train loops.
- `src/experiments`: runnable experiment entrypoints.
- `src/data`: Fashion-like synthetic proxy + optics-native task.
- `src/viz`: plotting/report utilities.
- `tests/`: smoke and reproducibility tests.
- `outputs/`: checkpoints, CSV logs, plots.
- `docs/progress/`: markdown summaries of experiment progress.

## Topic 1 follow-up (torch-focused)

- Torch pilot config: `configs/topic1/pilot_torch.yaml`
- Torch pilot runner: `bash scripts/run_topic1_torch_pilot.sh`
- Backend comparison runner: `bash scripts/run_topic1_backend_compare.sh`
- Progress index: `docs/progress/topic1_progress_index.md`
