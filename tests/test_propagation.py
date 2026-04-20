import unittest

from src.core.propagation import angular_spectrum_propagate, fresnel_propagate


class TestPropagation(unittest.TestCase):
    def test_shapes(self):
        field = [[1.0 for _ in range(8)] for _ in range(8)]
        self.assertEqual(len(angular_spectrum_propagate(field, 532e-9, 0.03, 1.2e-5)), 8)
        self.assertEqual(len(fresnel_propagate(field, 532e-9, 0.03, 1.2e-5)[0]), 8)


if __name__ == "__main__":
    unittest.main()
