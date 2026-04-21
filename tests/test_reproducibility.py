import random
import unittest

from src.core.utils import set_seed


class TestRepro(unittest.TestCase):
    def test_seed_reproducibility(self):
        set_seed(123)
        a = [random.random() for _ in range(3)]
        set_seed(123)
        b = [random.random() for _ in range(3)]
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
