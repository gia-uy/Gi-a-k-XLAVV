
# ScanCare — Nâng cao chất lượng tài liệu Scan

## Giới thiệu

ScanCare là ứng dụng web hỗ trợ nâng cao chất lượng
ảnh tài liệu scan hoặc ảnh chụp.

Phiên bản hiện tại chỉ xây dựng giao diện bằng Streamlit.
Các thuật toán xử lý ảnh chưa được kết nối.

## Công nghệ

- Python
- Streamlit
- OpenCV
- NumPy
- Pillow

## Chạy ứng dụng

Tạo môi trường ảo, cài đặt thư viện và chạy:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

# ScanCare — Quy tắc Logic & Gợi ý Thông minh (System & User Logic)

Tài liệu này định nghĩa toàn bộ quy tắc hoạt động của các nút bấm trên giao diện, ma trận kết hợp 6 thuật toán xử lý ảnh OpenCV (Backend) và các cơ chế gợi ý thông minh (Smart Defaults & Auto-rules) hỗ trợ người dùng.

---

## I. LOGIC NÚT BẤM & TÙY CHỌN TRÊN GIAO DIỆN

### 1. Mức độ lọc nhiễu (Noise Level) — Radio Button
* **Mức Nhẹ:**
  * **Thuật toán Backend:** Lọc Gaussian (Gaussian Filter) với Kernel $3 \times 3$.
  * **Mục đích:** Xử lý ảnh mờ nhẹ, bụi mịn, bảo tồn tối đa chi tiết và các nét chữ mảnh.
  * **Gợi ý UX:** Dành cho tài liệu còn khá mới, ảnh chụp thẳng, rõ nét.
* **Mức Vừa (Mặc định):**
  * **Thuật toán Backend:** Lọc Trung vị (Median Filter) với Kernel $3 \times 3$.
  * **Mục đích:** Loại bỏ các đốm nhiễu đốm tiêu, vết bẩn trung bình trên nền giấy xám.
  * **Gợi ý UX:** Phù hợp với đa số tài liệu scan văn phòng thông thường.
* **Mức Mạnh:**
  * **Thuật toán Backend:** Lọc Trung vị (Median Filter) với Kernel $5 \times 5$.
  * **Mục đích:** Triệt phá các mảng nhiễu nặng, ảnh bị rỗ, nền giấy cũ sần sùi.
  * **Gợi ý UX:** Dành cho tài liệu cũ, bị ố vàng hoặc rỗ nặng.

---

### 2. Tăng độ tương phản (Contrast Enhancement) — Checkbox
* **Thuật toán Backend:** Kéo giãn tương phản (Contrast Stretching / Normalize).
* **Trạng thái mặc định:** **BẬT (Checked)**.
* **Quy tắc gợi ý thông minh:**
  * Thuật toán này an toàn cho **MỌI** loại tài liệu (kể cả ảnh màu, con dấu đỏ, văn bản).
  * **Nên bật khi:** Chữ bị nhạt màu, nền giấy xám/tối.
  * **Tắt khi:** Ảnh đã có độ tương phản quá cao, chữ bị đen đậm hoặc quá gắt.

---

### 3. Chuyển về Đen - Trắng thuần (Binarization & Morphology) — Checkbox
* **Thuật toán Backend:** Nhị phân hóa Otsu (Otsu Thresholding) + Phép Mở (Opening) + Phép Đóng (Closing).
* **Trạng thái mặc định:** **TẮT (Unchecked)**.
* **Quy tắc gợi ý thông minh:**
  * **NÊN chọn khi:** Tài liệu thuần văn bản đen trắng, muốn tẩy sạch 100% nền xám và bóng mờ.
  * **KHÔNG chọn khi:** Tài liệu có **con dấu đỏ**, **ảnh chụp chân dung**, hoặc **hình vẽ màu** (vì nhị phân hóa sẽ biến các vùng màu thành đen hoặc biến mất).

---

## II. MA TRẬN PHỐI HỢP 6 THUẬT TOÁN (PIPELINE)

Khi người dùng nhấn nút **"Nâng cao chất lượng tài liệu"**, Backend sẽ thực thi chuỗi 6 thuật toán theo đúng thứ tự logic bên dưới:

$$\text{Ảnh gốc} \xrightarrow{\text{Bước 1}} \text{Lọc nhiễu} \xrightarrow{\text{Bước 2}} \text{Kéo giãn tương phản} \xrightarrow{\text{Bước 3}} \text{Nhị phân hóa} \xrightarrow{\text{Bước 4}} \text{Phép Mở \& Phép Đóng} \rightarrow \text{Kết quả}$$

| Tùy chọn người dùng | 1. Lọc nhiễu (Filtering) | 2. Tăng tương phản | 3. Nhị phân hóa | 4. Xử lý hình thái (Morphology) |
| :--- | :--- | :--- | :--- | :--- |
| **Mức Nhẹ** | **Gaussian Filter** ($3 \times 3$) | **Contrast Stretching** *(nếu bật)* | **Otsu Thresholding** *(nếu bật)* | **Phép Đóng (Closing)** với Kernel $2 \times 2$<br>$\rightarrow$ *Nối nhẹ các nét chữ bị đứt mờ.* |
| **Mức Vừa** | **Median Filter** ($3 \times 3$) | **Contrast Stretching** *(nếu bật)* | **Otsu Thresholding** *(nếu bật)* | **Phép Mở (Opening)** $3 \times 3 \rightarrow$ **Phép Đóng (Closing)** $3 \times 3$<br>$\rightarrow$ *Mở để dọn hạt bẩn nền, Đóng để liền nét.* |
| **Mức Mạnh** | **Median Filter** ($5 \times 5$) | **Contrast Stretching** *(nếu bật)* | **Otsu Thresholding** *(nếu bật)* | **Phép Mở (Opening)** $3 \times 3 \rightarrow$ **Phép Đóng (Closing)** $4 \times 4$<br>$\rightarrow$ *Mở dọn mảng nhiễu rỗ, Đóng bù lại độ dầy chữ.* |

---

## III. QUY TẮC TỰ ĐỘNG THÔNG MINH (SMART AUTO-RULES)

Để tối ưu trải nghiệm và tránh lỗi thao tác người dùng, hệ thống áp dụng các quy tắc tự động hóa (Auto-trigger):

1. **Auto-Select khi đổi mức độ:**
   * Khi người dùng chuyển sang **Mức Mạnh**, hệ thống tự động gợi ý bật ô **Chuyển về Đen - Trắng thuần** (vì ảnh nhiễu nặng đa số cần nhị phân hóa để dọn sạch).
   * Khi chuyển về **Mức Nhẹ**, hệ thống tự động trả ô **Chuyển về Đen - Trắng thuần** về trạng thái **Tắt** để bảo toàn chi tiết gốc.
2. **An toàn dữ liệu màu (Color Safety Guarantee):**
   * Nếu ô *Chuyển về Đen - Trắng thuần* bị **Tắt**, bước 3 & 4 (Thresholding, Opening, Closing) sẽ được bỏ qua hoàn toàn để giữ nguyên màu con dấu đỏ và hình ảnh.
3. **Thứ tự bắt buộc của Morphology:**
   * Phép Mở (Opening) và Phép Đóng (Closing) **chỉ chạy ở Bước 4 sau khi đã Nhị phân hóa**, đảm bảo không làm biến dạng dải màu xám của ảnh gốc.