
import unittest
import numpy as np

from pipeline import process_image


class TestPipeline(unittest.TestCase):
    def setUp(self):
        # Tao anh tai lieu gia lap: nen trang, chu den
        self.image = np.full((100, 100), 255, dtype=np.uint8)
        self.image[30:70, 30:70] = 0

    def test_empty_steps_returns_copy(self):
        result = process_image(self.image, [])

        np.testing.assert_array_equal(result, self.image)
        self.assertIsNot(result, self.image)

    def test_median_filter(self):
        result = process_image(
            self.image, [{"method": "median_filter"}]
        )
        self.assertEqual(result.shape, self.image.shape)

    def test_gaussian_filter(self):
        result = process_image(
            self.image, [{"method": "gaussian_filter"}]
        )
        self.assertEqual(result.shape, self.image.shape)

    def test_contrast_stretching(self):
        result = process_image(
            self.image, [{"method": "contrast_stretching"}]
        )
        self.assertEqual(result.ndim, 2)

    def test_histogram_equalization(self):
        result = process_image(
            self.image, [{"method": "histogram_equalization"}]
        )
        self.assertEqual(result.ndim, 2)

    def test_binarization(self):
        result = process_image(
            self.image, [{"method": "binarization"}]
        )
        self.assertEqual(result.ndim, 2)
        self.assertTrue(set(np.unique(result)).issubset({0, 255}))

    def test_morphology(self):
        for method in ["erosion", "dilation", "opening", "closing"]:
            with self.subTest(method=method):
                result = process_image(
                    self.image, [{"method": method}]
                )
                self.assertEqual(result.shape, self.image.shape)

    def test_invalid_method(self):
        with self.assertRaises(ValueError):
            process_image(
                self.image, [{"method": "invalid_method"}]
            )


if __name__ == "__main__":
    unittest.main()
