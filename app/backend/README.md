# ScanCare — FastAPI tích hợp với phiên bản mới của An

Đây là bản làm việc **từ FastAPI V2 của Diệp**, thay thế thư viện xử lý bên trong bằng các file mới An bàn giao: `modules/filtering.py`, `contrast.py`, `morphology.py`, `auto_enhance.py`, và `pipeline.py`. Các hàm thuật toán được giữ nguyên.

## Chạy trong VS Code (Windows)

```powershell
cd backend
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Mở http://127.0.0.1:8000/docs và thử lần lượt `GET /health`, `POST /api/process`, `POST /api/auto-enhance`.

- `POST /api/auto-enhance`: multipart form `file` và `level` (`nhe`, `vua`, `manh`, hoặc tên tiếng Việt). Trả **PNG binary**, metadata trong header `X-Processing-Metadata`.
- `POST /api/analyze`: multipart form `file`, trả JSON số liệu tham khảo.
- `POST /api/process`: multipart form `file` và `steps` (JSON text), dùng `pipeline.process_image()` nguyên bản của An; hỗ trợ tên `method` hoặc cặp `operation/params`.
- `POST /api/export/image`: xuất PNG/JPG.
- `POST /api/export/pdf`: PDF dạng ảnh, là chức năng bổ sung.

## Điểm chưa thống nhất trước khi nối giao diện Uy

- Streamlit hiện dùng hàm Pillow demo tại `process_document()`, **chưa gửi HTTP request**.
- README của Uy nêu Otsu + Opening/Closing theo mức lọc, nhưng phiên bản mới của An **chưa có Otsu** và `auto_enhance()` chỉ có quy tắc Gaussian theo chỉ số Laplacian + Contrast Stretching theo std (chưa được xác thực). API không âm thầm triển khai thêm thuật toán.
- An gọi mức trung bình là `Trung bình`, Uy gọi là `Vừa`; adapter FastAPI ánh xạ hai tên.
- `modules/morphology.py` chỉ nhận kernel lẻ; cấu hình 2x2/4x4 trong README của Uy chưa tương thích.
- API tự động hiện không có lựa chọn bật/tắt contrast/binarization riêng của Uy. Trước khi kết nối UI cần chốt phạm vi với An hoặc thêm adapter/tính năng được thống nhất.
- Luồng API trả ảnh PNG trực tiếp và metadata ở header, nên Uy cần đọc `response.content` và `response.headers['X-Processing-Metadata']` (không thể gọi `response.json()` cho ảnh).

**Không nên merge đè những file gốc trong `Diep/`, `An/`, `Uy/`:** bản này phục vụ chạy thử trong `app/backend` riêng.

## Kiểm thử

```powershell
python -m pytest tests/test_spec.py -q
```
