
import unittest

import numpy as np

from modules.filtering import median_filter, gaussian_filter


class TestFiltering(unittest.TestCase):
    def setUp(self):
        self.image = np.zeros((20, 20), dtype=np.uint8)
        self.image[5:15, 5:15] = 200

    def test_median_filter_returns_image(self):
        result = median_filter(self.image, kernel_size=3)

        self.assertEqual(result.shape, self.image.shape)
        self.assertEqual(result.dtype, np.uint8)
        self.assertFalse(np.shares_memory(result, self.image))

    def test_gaussian_filter_returns_image(self):
        result = gaussian_filter(self.image, kernel_size=3)

        self.assertEqual(result.shape, self.image.shape)
        self.assertEqual(result.dtype, np.uint8)
        self.assertFalse(np.shares_memory(result, self.image))

    def test_invalid_image_raises_error(self):
        with self.assertRaises(ValueError):
            median_filter(None)

        with self.assertRaises(ValueError):
            gaussian_filter(None)

    def test_even_kernel_raises_error(self):
        with self.assertRaises(ValueError):
            median_filter(self.image, kernel_size=4)

        with self.assertRaises(ValueError):
            gaussian_filter(self.image, kernel_size=4)


if __name__ == "__main__":
    unittest.main()
