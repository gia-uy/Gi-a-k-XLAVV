
import unittest
import numpy as np

from modules.contrast import (
    contrast_stretching,
    histogram_equalization,
    binarization,
)


class TestContrast(unittest.TestCase):
    def setUp(self):
        self.image = np.array(
            [
                [50, 60, 70, 80],
                [90, 100, 110, 120],
                [130, 140, 150, 160],
                [170, 180, 190, 200],
            ],
            dtype=np.uint8,
        )

    def test_contrast_stretching_returns_image(self):
        result = contrast_stretching(self.image)

        self.assertEqual(result.shape, self.image.shape)
        self.assertEqual(result.dtype, np.uint8)
        self.assertEqual(int(result.min()), 0)
        self.assertEqual(int(result.max()), 255)

    def test_histogram_equalization_returns_image(self):
        result = histogram_equalization(self.image)

        self.assertEqual(result.shape, self.image.shape)
        self.assertEqual(result.dtype, np.uint8)

    def test_binarization_returns_binary_image(self):
        result = binarization(self.image, thresh_val=127)

        self.assertEqual(result.shape, self.image.shape)
        self.assertEqual(result.dtype, np.uint8)
        self.assertTrue(set(np.unique(result)).issubset({0, 255}))

    def test_invalid_image_raises_error(self):
        with self.assertRaises(ValueError):
            contrast_stretching(None)

        with self.assertRaises(ValueError):
            histogram_equalization(None)

        with self.assertRaises(ValueError):
            binarization(None)

    def test_invalid_threshold_raises_error(self):
        with self.assertRaises(ValueError):
            binarization(self.image, thresh_val=300)


if __name__ == "__main__":
    unittest.main()
