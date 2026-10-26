import cv2
import numpy as np
import matplotlib.pyplot as plt

def contrast_stretching(gray_img):
    r_min = float(np.min(gray_img))
    r_max = float(np.max(gray_img))
    
    if r_max == r_min:
        return gray_img
    
    stretched = (gray_img - r_min) * (255.0 / (r_max - r_min))
    stretched = np.clip(stretched, 0, 255) 
    return np.uint8(stretched)

def histogram_equalization(gray_img):
    return cv2.equalizeHist(gray_img)

def binarization(gray_img, thresh_val=127):
    _, binary_img = cv2.threshold(gray_img, thresh_val, 255, cv2.THRESH_BINARY)
    return binary_img

def main():
    img_path = 'scan_input.jpg'  #
    img = cv2.imread(img_path)
    
    if img is None:
        print(f"Lỗi: Không tìm thấy file ảnh tại '{img_path}'. Hãy kiểm tra lại tên file.")
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img_stretched = contrast_stretching(gray)
    img_equ = histogram_equalization(gray)
    img_binary = binarization(img_stretched, thresh_val=130)

    cv2.imwrite('result_contrast_stretching.jpg', img_stretched)
    cv2.imwrite('result_histogram_equalization.jpg', img_equ)
    cv2.imwrite('result_binarization.jpg', img_binary)
    print("Đã lưu các ảnh kết quả thành công!")

    plt.figure(figsize=(12, 8))

    plt.subplot(2, 4, 1)
    plt.imshow(gray, cmap='gray')
    plt.title("Ảnh gốc (Gray)")
    plt.axis("off")

    plt.subplot(2, 4, 5)
    hist_gray = cv2.calcHist([gray], [0], None, [256], [0, 256])
    plt.plot(hist_gray, color='black')
    plt.title("Histogram Gốc")

    plt.subplot(2, 4, 2)
    plt.imshow(img_stretched, cmap='gray')
    plt.title("Contrast Stretching")
    plt.axis("off")

    plt.subplot(2, 4, 6)
    hist_stretch = cv2.calcHist([img_stretched], [0], None, [256], [0, 256])
    plt.plot(hist_stretch, color='blue')
    plt.title("Histogram Kéo giãn")

    plt.subplot(2, 4, 3)
    plt.imshow(img_equ, cmap='gray')
    plt.title("Equalization")
    plt.axis("off")

    plt.subplot(2, 4, 7)
    hist_equ = cv2.calcHist([img_equ], [0], None, [256], [0, 256])
    plt.plot(hist_equ, color='red')
    plt.title("Histogram Cân bằng")

    plt.subplot(2, 4, 4)
    plt.imshow(img_binary, cmap='gray')
    plt.title("Nhị phân (Binarization)")
    plt.axis("off")

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()