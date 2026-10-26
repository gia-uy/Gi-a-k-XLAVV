
import cv2
import numpy as np

from image_processing import median_filter, gaussian_filter
from an_algorithms import (
    contrast_stretching,
    histogram_equalization,
    binarization,
)
from Diep.morphology import apply_morphology


def process_image(image, steps):
    """
    Xử lý ảnh theo danh sách các bước.

    image: ảnh OpenCV dạng numpy.ndarray.
    steps: danh sách các bước xử lý theo thứ tự.

    Ví dụ:
    [
        {"method": "contrast_stretching"},
        {"method": "median_filter", "kernel_size": 3},
        {"method": "binarization", "threshold": 127}
    ]
    """
    if image is None or not isinstance(image, np.ndarray) or image.size == 0:
        raise ValueError("Ảnh đầu vào không hợp lệ.")

    result = image.copy()

    for step in steps:
        method = step.get("method")

        if method == "contrast_stretching":
            gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY) if result.ndim == 3 else result
            result = contrast_stretching(gray)

        elif method == "histogram_equalization":
            gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY) if result.ndim == 3 else result
            result = histogram_equalization(gray)

        elif method == "binarization":
            gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY) if result.ndim == 3 else result
            threshold = step.get("threshold", 127)
            result = binarization(gray, threshold)

        elif method == "median_filter":
            result = median_filter(result, step.get("kernel_size", 3))

        elif method == "gaussian_filter":
            result = gaussian_filter(
                result,
                step.get("kernel_size", 3),
                step.get("sigma", 0),
            )

        elif method in {"erosion", "dilation", "opening", "closing"}:
            result = apply_morphology(
                result,
                method=method,
                kernel_size=step.get("kernel_size", 3),
                shape=step.get("shape", "rect"),
                threshold=step.get("threshold", 127),
                iterations=step.get("iterations", 1),
            )

        else:
            raise ValueError(f"Thuật toán không hợp lệ: {method}")

    return result
