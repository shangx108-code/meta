#!/usr/bin/env bash
set -euo pipefail
python -m src.experiments.topic1_compare_backends --config configs/topic1/pilot.yaml --output-dir outputs/topic1/backend_compare
