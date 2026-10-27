
import unittest
import numpy as np

from modules.morphology import (
    erosion,
    dilation,
    opening,
    closing,
    apply_morphology,
)


class TestMorphology(unittest.TestCase):
    def setUp(self):
        # Tạo ảnh nhị phân có một vùng trắng ở giữa
        self.image = np.zeros((20, 20), dtype=np.uint8)
        self.image[5:15, 5:15] = 255

    def test_erosion_returns_image(self):
        result = erosion(self.image, kernel_size=3)

        self.assertEqual(result.shape, self.image.shape)
        self.assertEqual(result.dtype, np.uint8)

    def test_dilation_returns_image(self):
        result = dilation(self.image, kernel_size=3)

        self.assertEqual(result.shape, self.image.shape)
        self.assertEqual(result.dtype, np.uint8)

    def test_opening_returns_image(self):
        result = opening(self.image, kernel_size=3)

        self.assertEqual(result.shape, self.image.shape)
        self.assertEqual(result.dtype, np.uint8)

    def test_closing_returns_image(self):
        result = closing(self.image, kernel_size=3)

        self.assertEqual(result.shape, self.image.shape)
        self.assertEqual(result.dtype, np.uint8)

    def test_invalid_image_raises_error(self):
        with self.assertRaises(ValueError):
            apply_morphology(None, method="erosion")

    def test_invalid_method_raises_error(self):
        with self.assertRaises(ValueError):
            apply_morphology(self.image, method="invalid")

    def test_invalid_kernel_raises_error(self):
        with self.assertRaises(ValueError):
            apply_morphology(self.image, method="erosion", kernel_size=2)


if __name__ == "__main__":
    unittest.main()
