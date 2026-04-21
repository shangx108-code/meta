#!/usr/bin/env bash
set -euo pipefail
python -m src.training.train_topic1 --config configs/topic1/smoke.yaml
