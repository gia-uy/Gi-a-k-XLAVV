# Thuật toán hình thái học – Diệp

Module độc lập cho Giai đoạn 1, dùng lại trong Giai đoạn 2 (FastAPI).

## Cài đặt

```bash
pip install opencv-python numpy
```

## Chạy thử

```bash
python demo.py tai_lieu.png
```

Kết quả lưu trong `ket_qua/` gồm ảnh gốc và 4 ảnh ứng với co, giãn, mở, đóng.

## Hợp đồng tích hợp cho An / Diệp

```python
from morphology import apply_morphology
result = apply_morphology(image, method='closing', kernel_size=3, shape='rect', threshold=127)
```

- Đầu vào `image`: mảng `numpy.ndarray`, xám uint8 hoặc BGR uint8.
- Đầu ra: ảnh xám uint8, chữ đen/nền trắng.
- `method`: `erosion`, `dilation`, `opening`, `closing`.
- `kernel_size`: nguyên 1–15 (khuyến nghị thử 2 hoặc 3 trước).
- `shape`: `rect`, `ellipse`, `cross`.
- `threshold`: ngưỡng nhị phân 0–255, mặc định 127.
- Ảnh đầu vào **bị nhị phân hóa** khi gọi hàm, cần chú ý vị trí trong pipeline.
- Với ảnh chữ trắng trên nền đen hoặc ảnh đã nhị phân đảo từ An, cần thống nhất/đảo lại quy ước trước khi gọi.
- Không tự lưu file, không phụ thuộc FastAPI. An có thể import trực tiếp và sử dụng trong `process_image(image, steps)`.
- **Không thay thế `pipeline.py` hiện có:** An vẫn chịu trách nhiệm tích hợp tất cả các phép toán.

## Lưu ý thực nghiệm

Phép mở trên tiền cảnh chữ trắng có thể xóa chấm nhiễu nhưng cũng có thể xóa dấu tiếng Việt. Phép đóng có thể nối khe đứt nhưng có thể làm dính ký tự. Các phép co/giãn thay đổi bề dày nét. Kernel 5x5 không phải lúc nào cũng phù hợp với chữ nhỏ. Chỉ áp dụng khi có hiệu quả qua kiểm thử.
