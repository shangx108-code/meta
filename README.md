# Optical Neural Network Research Simulation Platform

Simulation-first research codebase for three topics:
1. **Topic 1**: Broadband and partially-coherent robust diffractive optical neural networks under fabrication/alignment errors.
2. **Topic 2**: Device-aware nonlinear activation co-design for scalable optical neural networks.
3. **Topic 4**: Multiplexed multi-task optical neural networks via wavelength/polarization/spatial-mode DoFs.

## Quick start

```bash
bash scripts/setup_env.sh
bash scripts/run_topic1_smoke.sh
bash scripts/run_topic1_pilot.sh
bash scripts/run_topic2_smoke.sh
bash scripts/run_topic4_smoke.sh
bash scripts/report_status.sh
```

## Structure

- `configs/`: YAML configs for each topic.
- `src/core`: propagation, coherence, wavelength sampling, noise, and metrics.
- `src/models`: D2NN, nonlinear activations, multiplexing modules.
- `src/training`: training losses and train loops.
- `src/experiments`: runnable experiment entrypoints.
- `src/data`: Fashion-MNIST + synthetic optics-native task.
- `src/viz`: plotting and report utilities.
- `tests/`: smoke and reproducibility tests.
- `outputs/`: checkpoints, CSV logs, plots.
- `docs/progress/`: markdown summaries of experiment progress.

## Reproducibility

- deterministic seed utilities included
- compact defaults designed for CPU/sandbox execution
- pilot-first then larger sweeps
