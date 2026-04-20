import unittest

from src.models.d2nn import D2NN, DetectorHead


class TestShapes(unittest.TestCase):
    def test_d2nn_detector_shape_consistency(self):
        model = D2NN(image_size=8, num_layers=1, propagation_distance=0.02, pixel_size=1e-5)
        head = DetectorHead(8, 10)
        x = [[0.5 for _ in range(8)] for _ in range(8)]
        intensity = model.forward_wavelength(x, 532e-9, {"phase_quantization_bits": 4})
        logits = head.forward(intensity)
        self.assertEqual(len(logits), 10)


if __name__ == "__main__":
    unittest.main()
