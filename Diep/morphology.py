import cv2
import numpy as np

SHAPES = {"rect": cv2.MORPH_RECT, "ellipse": cv2.MORPH_ELLIPSE, "cross": cv2.MORPH_CROSS}
METHODS = {"erosion", "dilation", "opening", "closing"}


def _binary_foreground(image: np.ndarray, threshold: int = 127) -> np.ndarray:
    if image is None or not isinstance(image, np.ndarray) or image.size == 0:
        raise ValueError("Ảnh đầu vào không hợp lệ")
    if image.dtype != np.uint8:
        raise ValueError("Ảnh phải có kiểu uint8")
    if image.ndim == 3 and image.shape[2] == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif image.ndim == 2:
        gray = image
    else:
        raise ValueError("Chỉ hỗ trợ ảnh xám hoặc ảnh BGR 3 kênh")
    if not 0 <= threshold <= 255:
        raise ValueError("threshold phải từ 0 đến 255")
    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)
    return binary


def apply_morphology(image: np.ndarray, method: str, kernel_size: int = 3,
                     shape: str = "rect", threshold: int = 127,
                     iterations: int = 1) -> np.ndarray:
    """Trả ảnh nhị phân chữ đen/nền trắng sau hình thái học."""
    if method not in METHODS:
        raise ValueError(f"Phương pháp không hợp lệ: {method}")
    if type(kernel_size) is not int or not 1 <= kernel_size <= 15:
        raise ValueError("kernel_size phải là số nguyên từ 1 đến 15")
    if shape not in SHAPES:
        raise ValueError(f"shape phải thuộc {list(SHAPES)}")
    if type(iterations) is not int or not 1 <= iterations <= 5:
        raise ValueError("iterations phải là số nguyên từ 1 đến 5")
    foreground = _binary_foreground(image, threshold)
    kernel = cv2.getStructuringElement(SHAPES[shape], (kernel_size, kernel_size))
    if method == "erosion":
        result = cv2.erode(foreground, kernel, iterations=iterations)
    elif method == "dilation":
        result = cv2.dilate(foreground, kernel, iterations=iterations)
    else:
        operation = cv2.MORPH_OPEN if method == "opening" else cv2.MORPH_CLOSE
        result = cv2.morphologyEx(foreground, operation, kernel, iterations=iterations)
    return cv2.bitwise_not(result)


def erosion(image, kernel_size=3, shape="rect", threshold=127):
    return apply_morphology(image, "erosion", kernel_size, shape, threshold)


def dilation(image, kernel_size=3, shape="rect", threshold=127):
    return apply_morphology(image, "dilation", kernel_size, shape, threshold)


def opening(image, kernel_size=3, shape="rect", threshold=127):
    return apply_morphology(image, "opening", kernel_size, shape, threshold)


def closing(image, kernel_size=3, shape="rect", threshold=127):
    return apply_morphology(image, "closing", kernel_size, shape, threshold)
