import csv
import json
import unittest
from pathlib import Path

from src.experiments.topic1_pilot import run_pilot


class TestTopic1FlatSweepGuard(unittest.TestCase):
    def test_pairwise_deltas_not_all_flat(self):
        cfg = {
            "seed": 23,
            "image_size": 16,
            "batch_size": 8,
            "epochs": 1,
            "train_samples": 24,
            "val_samples": 12,
            "lr": 0.03,
            "num_layers": 1,
            "propagation_distance": 0.03,
            "pixel_size": 1.2e-5,
            "wavelengths_nm": [530],
            "coherence_grid": [1.0, 0.6],
            "bandwidth_grid": [[530], [510, 530, 550]],
            "misalignment_grid": [
                {"lateral_shift_px": 0.0, "axial_shift_scale": 0.0, "phase_error_std": 0.0, "loss_error_std": 0.0},
                {"lateral_shift_px": 1.0, "axial_shift_scale": 0.2, "phase_error_std": 0.2, "loss_error_std": 0.1},
            ],
            "phase_quantization_bits": 5,
            "phase_quantization_bits_grid": [4, 6],
            "noise_sigma": 0.02,
            "efficiency_weight": 0.05,
            "robust_weight": 0.2,
            "output_dir": "outputs/topic1/test_flat_guard",
            "backend": "surrogate",
        }
        cfg_path = Path("outputs/topic1/test_flat_guard_cfg.json")
        cfg_path.parent.mkdir(parents=True, exist_ok=True)
        cfg_path.write_text(json.dumps(cfg), encoding="utf-8")

        run_pilot(str(cfg_path))

        with open("outputs/topic1/test_flat_guard/pilot_sweep.csv", "r", encoding="utf-8") as f:
            sweep_rows = list(csv.DictReader(f))
        acc_values = [float(r["val_acc"]) for r in sweep_rows]
        self.assertGreater(max(acc_values) - min(acc_values), 0.01)

        with open("outputs/topic1/test_flat_guard/ablation_pairwise.csv", "r", encoding="utf-8") as f:
            pair_rows = list(csv.DictReader(f))
        deltas = [abs(float(r["delta_a_minus_b"])) for r in pair_rows]
        self.assertTrue(any(d > 0.005 for d in deltas), "all pairwise deltas are near-zero; sweep may be collapsed")


if __name__ == "__main__":
    unittest.main()
