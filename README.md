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

