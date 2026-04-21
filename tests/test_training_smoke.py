import unittest
from pathlib import Path

from src.training.train_topic1 import run_topic1


class TestTrainingSmoke(unittest.TestCase):
    def test_topic1_training_path_smoke(self):
        cfg = Path("outputs/topic1/test_cfg.json")
        cfg.parent.mkdir(parents=True, exist_ok=True)
        cfg.write_text('{"seed":3,"image_size":16,"batch_size":8,"epochs":1,"train_samples":16,"val_samples":8,"lr":0.01,"num_layers":1,"propagation_distance":0.02,"pixel_size":1.2e-5,"wavelengths_nm":[530],"coherence_mix":1.0,"noise_sigma":0.01,"robust_training":false,"phase_quantization_bits":4,"output_dir":"outputs/topic1/test_smoke"}', encoding="utf-8")
        metrics_path = run_topic1(str(cfg))
        self.assertTrue(metrics_path.endswith("metrics.csv"))


if __name__ == "__main__":
    unittest.main()
