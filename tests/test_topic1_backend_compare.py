import csv
import json
import unittest
from pathlib import Path

from src.experiments.topic1_compare_backends import compare


class TestTopic1BackendCompare(unittest.TestCase):
    def test_compare_generates_status_table(self):
        cfg = {
            "seed": 5,
            "image_size": 16,
            "batch_size": 8,
            "epochs": 1,
            "train_samples": 16,
            "val_samples": 8,
            "lr": 0.01,
            "num_layers": 1,
            "propagation_distance": 0.03,
            "pixel_size": 1.2e-5,
            "wavelengths_nm": [530],
            "coherence_grid": [1.0],
            "bandwidth_grid": [[530], [510, 530, 550]],
            "misalignment_grid": [
                {"lateral_shift_px": 0.0, "axial_shift_scale": 0.0, "phase_error_std": 0.0, "loss_error_std": 0.0},
                {"lateral_shift_px": 1.0, "axial_shift_scale": 0.1, "phase_error_std": 0.1, "loss_error_std": 0.05},
            ],
            "phase_quantization_bits": 4,
            "noise_sigma": 0.01,
            "efficiency_weight": 0.05,
            "robust_weight": 0.2,
            "output_dir": "outputs/topic1/test_backend_compare_base",
            "backend": "auto",
        }
        cfg_path = Path("outputs/topic1/test_backend_compare_cfg.json")
        cfg_path.write_text(json.dumps(cfg), encoding="utf-8")
        out_dir = "outputs/topic1/test_backend_compare"
        compare(str(cfg_path), out_dir)
        with open(f"{out_dir}/backend_comparison.csv", "r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertGreaterEqual(len(rows), 1)
        self.assertIn(rows[0]["status"], {"ok", "torch_unavailable"})


if __name__ == "__main__":
    unittest.main()
