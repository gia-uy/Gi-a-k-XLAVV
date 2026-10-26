# Image Filtering Algorithms

Dự án cài đặt hai thuật toán lọc ảnh cơ bản bằng Python và OpenCV, phục vụ cho đề tài xử lý ảnh của nhóm.

Hai thuật toán được triển khai:
- **Median Filter:** Lọc nhiễu muối tiêu (Salt-and-Pepper Noise).
- **Gaussian Filter:** Làm mượt ảnh và hỗ trợ giảm nhiễu Gaussian.

Chương trình cho phép lựa chọn thuật toán, thiết lập kích thước kernel, hiển thị ảnh sau xử lý và lưu ảnh kết quả để so sánh với ảnh gốc.


## 1.Cấu trúc thư mục

```text
image_processing_project/
├── image_processing.py
├── input_images/
│   └── test.jpg
├── output_images/
└── README.md
```

Trong đó:
- `image_processing.py`: Cài đặt hai thuật toán lọc ảnh và chương trình chạy thử.
- `input_images/`: Chứa ảnh đầu vào.
- `output_images/`: Lưu ảnh sau khi xử lý.
- `README.md`: Tài liệu hướng dẫn sử dụng dự án.

## 2. Chức năng

### 2.1. Median Filter

Median Filter thay thế giá trị của mỗi pixel bằng giá trị trung vị của các pixel trong vùng lân cận.

**Mục đích:**
- Loại bỏ nhiễu muối tiêu.
- Hạn chế ảnh hưởng của các pixel nhiễu có giá trị quá cao hoặc quá thấp.
- Giúp giữ biên ảnh tương đối tốt.

Hàm xử lý:

```python
median_filter(image, kernel_size=3)
```

### 2.2. Gaussian Filter

Gaussian Filter sử dụng kernel Gaussian để tính toán giá trị pixel mới thông qua phép tích chập.

**Mục đích:**
- Làm mượt ảnh.
- Hỗ trợ giảm nhiễu Gaussian.
- Giảm các biến đổi cường độ pixel nhỏ trong ảnh.

Hàm xử lý:

```python
gaussian_filter(image, kernel_size=3, sigma=0)
```

Trong đó, `sigma=0` cho phép OpenCV tự xác định độ lệch chuẩn phù hợp với kích thước kernel.

### 2.3. Lựa chọn kích thước kernel

Chương trình hỗ trợ thử nghiệm các kích thước kernel:

- `3×3`
- `5×5`
- `7×7`

Kernel có kích thước càng lớn thì mức độ làm mượt hoặc lọc nhiễu thường càng mạnh, nhưng cũng có thể làm mất chi tiết ảnh.

## 3. Cài đặt môi trường

Yêu cầu Python đã được cài đặt trên máy tính.

Cài đặt các thư viện cần thiết:

```bash
pip install opencv-python numpy
```

## 4. Hướng dẫn sử dụng

**Bước 1:** Đặt ảnh cần xử lý vào thư mục `input_images/` và đặt tên là `test.jpg`.

**Bước 2:** Mở Terminal tại thư mục dự án.

**Bước 3:** Chạy chương trình:

```bash
python image_processing.py
```

**Bước 4:** Quan sát các cửa sổ hiển thị ảnh gốc, ảnh sau khi áp dụng Median Filter và ảnh sau khi áp dụng Gaussian Filter.

**Bước 5:** Kiểm tra ảnh kết quả được lưu trong thư mục `output_images/`.

Các ảnh kết quả mặc định:
- `median_3x3.jpg`
- `gaussian_3x3.jpg`

Để thay đổi kích thước kernel, chỉnh tham số `kernel_size` trong lời gọi hàm xử lý.

## 5. Kết quả đầu ra

Chương trình tạo hai ảnh kết quả để so sánh với ảnh ban đầu:

| Tên file | Thuật toán |
|---|---|
| `median_3x3.jpg` | Median Filter |
| `gaussian_3x3.jpg` | Gaussian Filter |

Hiệu quả của từng thuật toán phụ thuộc vào loại nhiễu, kích thước kernel và đặc điểm của ảnh đầu vào.


## Pipeline tích hợp các thuật toán xử lý ảnh

Dự án tích hợp các thuật toán xử lý ảnh của các thành viên vào một pipeline chung, cho phép thực hiện nhiều bước xử lý theo thứ tự do người dùng lựa chọn.

### 1. Các thuật toán được tích hợp

**Nhóm thuật toán của An — Cải thiện độ tương phản và nhị phân hóa**
- Contrast Stretching: Kéo giãn độ tương phản ảnh.
- Histogram Equalization: Cân bằng histogram ảnh xám.
- Binarization: Nhị phân hóa ảnh theo ngưỡng.

**Nhóm thuật toán của Uy — Bộ lọc ảnh**
- Median Filter: Lọc trung vị để giảm nhiễu.
- Gaussian Filter: Làm mượt ảnh bằng bộ lọc Gaussian.

**Nhóm thuật toán của Diệp — Hình thái học**
- Erosion: Co đối tượng.
- Dilation: Giãn đối tượng.
- Opening: Kết hợp co và giãn để hỗ trợ loại bỏ nhiễu nhỏ.
- Closing: Kết hợp giãn và co để hỗ trợ lấp các khoảng trống nhỏ.

### 2. Cấu trúc các file chính

- `image_processing.py`: Chứa Median Filter, Gaussian Filter và hàm lưu ảnh.
- `an_algorithms.py`: Chứa ba thuật toán của An.
- `Diep/morphology.py`: Chứa bốn thuật toán hình thái học của Diệp.
- `pipeline.py`: Tích hợp và thực thi các thuật toán theo thứ tự.
- `input_images/`: Chứa ảnh đầu vào.
- `output_images/`: Chứa ảnh kết quả mẫu.

### 3. Cách sử dụng pipeline

Tạo file Python hoặc chạy đoạn mã sau tại thư mục gốc của dự án:

```python
import cv2
from pipeline import process_image

image = cv2.imread("input_images/anhtest1.webp")

if image is None:
    raise FileNotFoundError("Không tìm thấy ảnh đầu vào.")

steps = [
    {"method": "contrast_stretching"},
    {"method": "median_filter", "kernel_size": 3},
    {"method": "binarization", "threshold": 127},
]

result = process_image(image, steps)

cv2.imwrite("output_images/pipeline_result.jpg", result)
print("Đã xử lý và lưu ảnh thành công!")
```

### 4. Chạy chương trình

Cài đặt các thư viện cần thiết nếu máy chưa có:

```bash
pip install opencv-python numpy
```

Chạy đoạn mã sử dụng pipeline từ thư mục gốc của dự án. Có thể thay đổi danh sách `steps` để lựa chọn thuật toán và thứ tự xử lý.

### 5. Kết quả kiểm thử

Đã kiểm tra việc import pipeline và thực thi độc lập cả 9 thuật toán trên ảnh đầu vào mẫu. Các thuật toán trả về ảnh kết quả theo định dạng mong đợi.

