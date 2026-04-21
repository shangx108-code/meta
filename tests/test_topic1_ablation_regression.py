import csv
import json
import unittest
from pathlib import Path

from src.experiments.topic1_pilot import run_pilot


class TestTopic1AblationRegression(unittest.TestCase):
    def test_ablation_has_nontrivial_deltas(self):
        cfg = {
            "seed": 23,
            "image_size": 16,
            "batch_size": 8,
            "epochs": 1,
            "train_samples": 24,
            "val_samples": 12,
            "lr": 0.02,
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
            "noise_sigma": 0.02,
            "efficiency_weight": 0.05,
            "robust_weight": 0.2,
            "output_dir": "outputs/topic1/test_ablation_regression",
            "backend": "surrogate",
        }
        cfg_path = Path("outputs/topic1/test_ablation_regression_cfg.json")
        cfg_path.write_text(json.dumps(cfg), encoding="utf-8")
        run_pilot(str(cfg_path))

        with open("outputs/topic1/test_ablation_regression/ablation_pairwise.csv", "r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), 4)
        deltas = [abs(float(r["delta_a_minus_b"])) for r in rows]
        self.assertGreater(max(deltas), 0.03, "ablation deltas should not collapse to near-zero")


if __name__ == "__main__":
    unittest.main()
