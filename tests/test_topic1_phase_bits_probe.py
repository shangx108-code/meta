import csv
import json
import unittest
from pathlib import Path

from src.experiments.topic1_pilot import run_pilot


class TestTopic1PhaseBitsProbe(unittest.TestCase):
    def test_phase_bits_probe_not_flat(self):
        cfg = {
            "seed": 29,
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
            "coherence_grid": [1.0],
            "bandwidth_grid": [[530], [510, 530, 550]],
            "misalignment_grid": [
                {"lateral_shift_px": 0.0, "axial_shift_scale": 0.0, "phase_error_std": 0.0, "loss_error_std": 0.0},
                {"lateral_shift_px": 1.0, "axial_shift_scale": 0.1, "phase_error_std": 0.1, "loss_error_std": 0.05},
            ],
            "phase_quantization_bits": 5,
            "phase_quantization_bits_grid": [3, 5, 7],
            "noise_sigma": 0.02,
            "efficiency_weight": 0.05,
            "robust_weight": 0.2,
            "output_dir": "outputs/topic1/test_phase_bits_probe",
            "backend": "surrogate",
        }
        cfg_path = Path("outputs/topic1/test_phase_bits_probe_cfg.json")
        cfg_path.write_text(json.dumps(cfg), encoding="utf-8")
        run_pilot(str(cfg_path))

        with open("outputs/topic1/test_phase_bits_probe/phase_bits_probe/phase_bits_sweep.csv", "r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        vals = {float(r["val_acc"]) for r in rows}
        self.assertGreater(len(rows), 1)
        self.assertGreater(len(vals), 1, "phase-bits probe should not collapse to a single metric")


if __name__ == "__main__":
    unittest.main()
