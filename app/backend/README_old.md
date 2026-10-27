# Backend FastAPI - Diệp (theo đặc tả của nhóm trưởng)

**Phạm vi:** FastAPI nhận ảnh từ giao diện (Streamlit hoặc web khác), kiểm tra ảnh, gọi `pipeline.py` của An, trả ảnh hoặc PDF và metadata. Không xây dựng UI thay Uy.

## Đối chiếu đặc tả
- Ảnh JPG/JPEG/PNG; giới hạn mặc định 10MB/20 triệu pixel.
- Phân tích sơ bộ: `POST /api/analyze` (chỉ số tương phản và biến thiên Laplacian, KHÔNG khẳng định phát hiện đúng loại nhiễu).
- Nút tự động: `POST /api/auto-enhance` với form `file`, `level`=`nhe|vua|manh`. Trả ảnh PNG; header `X-Processing-Metadata` là JSON gồm các bước, chỉ số và thời gian.
- Tùy chọn nâng cao: `POST /api/process` nhận form `file`, `steps` JSON. Hỗ trợ dạng `[{"operation":"median","params":{"kernel_size":3}}]` của bản requirements cũ **hoặc** `[{"method":"median_filter","kernel_size":3}]` của An.
- Lưu ảnh: `POST /api/export/image` form `file` (ảnh cần xuất), `format`=`png|jpg`. Trả file.
- PDF mở rộng từ kế hoạch trước: `POST /api/export/pdf`, form `files` (nhiều ảnh), `mode`=`as_is|manual|auto`; mặc định `as_is` nghĩa là các ảnh đã được xử lý sẵn, không xử lý lại.
- Hoàn tác, so sánh, zoom: UI của Uy giữ ảnh gốc và ảnh kết quả, **không yêu cầu backend lưu trạng thái**.

## Chạy
```powershell
cd backend
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn main:app --reload
```
Swagger: http://127.0.0.1:8000/docs
Test: `python -m pytest tests/test_spec.py -q`

## Tích hợp mã nhóm
- `backend/image_processing.py` là module **nguyên bản của Uy**.
- `backend/an_algorithms.py` và `backend/pipeline.py` là module **nguyên bản của An**.
- `backend/Diep/morphology.py` là module **nguyên bản của Diệp**.
- `backend/processing/pipeline.py` chỉ import lại hàm `process_image()` của An. Các bước `operation/params` được chuyển đổi bởi `services/contracts.py`; thuật toán gốc không bị thay.
- Khi nhóm di chuyển thư mục GitHub, sửa import hoặc đặt đường dẫn import phù hợp, không tạo bản sao thuật toán khác nhau.

## Ranh giới quan trọng
File `services/auto_enhance.py` là **bản thử nghiệm quy tắc sơ bộ**, do Diệp viết để API auto hoạt động trước; chưa được An xác nhận/kiểm thử. Hiện nó chọn Median kernel 3 hoặc 5 và thêm Contrast Stretching nếu khoảng p95−p5 dưới 90. **Không tự ý nói rằng đây là phát hiện loại nhiễu**. Không tự áp dụng Binarization hay Morphology vì nguy cơ mất dấu/nét chữ. An nên thay `plan()` bằng logic có dữ liệu kiểm thử, theo đặc tả trang 5–6.

Streamlit **không cần CORS** vì Python client gọi API từ server; CORS chỉ cần cho frontend trình duyệt gọi thẳng API.

### Ví dụ gửi ảnh từ Streamlit (cho Uy)
```python
import requests
response = requests.post(
    'http://127.0.0.1:8000/api/auto-enhance',
    files={'file': ('scan.png', image_bytes, 'image/png')},
    data={'level': 'vua'}, timeout=60,
)
response.raise_for_status()
result_bytes = response.content
import json
metadata = json.loads(response.headers['X-Processing-Metadata'])
```

**Chưa có:** OCR/DOCX, lịch sử phiên bản trên server. PDF dạng ảnh là mở rộng ngoài đặc tả mới (đặc tả chỉ yêu cầu lưu JPG/PNG).
