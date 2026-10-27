import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
from io import BytesIO

st.set_page_config(
    page_title="ScanCare | Nâng cao chất lượng tài liệu",
    page_icon="S",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ====================== SESSION STATE ======================
if "page" not in st.session_state:
    st.session_state.page = "upload"  # "upload" hoặc "result"

if "noise_level" not in st.session_state:
    st.session_state.noise_level = "Vừa"

if "enhance_contrast" not in st.session_state:
    st.session_state.enhance_contrast = True

if "binarize" not in st.session_state:
    st.session_state.binarize = False

if "image_original" not in st.session_state:
    st.session_state.image_original = None

if "image_processed" not in st.session_state:
    st.session_state.image_processed = None

if "file_name" not in st.session_state:
    st.session_state.file_name = "scancare_result.png"


# ====================== HÀM XỬ LÝ ĐỀ XUẤT (STUB) ======================
def process_document(image: Image.Image, noise_level: str, contrast: bool, binarize: bool) -> Image.Image:
    res = image.copy()
    
    # 1. Giảm nhiễu theo 3 mức độ
    if noise_level == "Nhẹ":
        res = res.filter(ImageFilter.SMOOTH)
    elif noise_level == "Vừa":
        res = res.filter(ImageFilter.GaussianBlur(radius=0.8))
    elif noise_level == "Mạnh":
        res = res.filter(ImageFilter.MedianFilter(size=3))

    # 2. Tăng tương phản
    if contrast:
        enhancer = ImageEnhance.Contrast(res)
        res = enhancer.enhance(1.6)

    # 3. Nhị phân hóa
    if binarize:
        gray = res.convert("L")
        threshold = 140
        res = gray.point(lambda p: 255 if p > threshold else 0).convert("RGB")

    return res


def image_to_bytes(img: Image.Image) -> bytes:
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# Cấu hình màu sắc & nội dung cho 3 mức độ lọc nhiễu
TIPS_CONFIG = {
    "Nhẹ": {
        "text": "Mức Nhẹ: Dành cho ảnh khá nét, chỉ bị mờ nhẹ hoặc có vài đốm li ti.",
        "style": "background-color: #fef3c7; border: 1px solid #fde68a; color: #92400e;"  # Màu Be / Vàng ấm
    },
    "Vừa": {
        "text": "Mức Vừa: Dành cho tài liệu có vết bẩn nhỏ, nền giấy hơi tối/xám.",
        "style": "background-color: #f0fdf4; border: 1px solid #bbf7d0; color: #166534;"  # Màu Xanh lá
    },
    "Mạnh": {
        "text": "Mức Mạnh: Dành cho ảnh bị rỗ, nhiễu nhiều. *(Lưu ý: Nét chữ cực mảnh có thể bị làm mờ)*",
        "style": "background-color: #fef2f2; border: 1px solid #fecaca; color: #991b1b;"  # Màu Đỏ
    }
}


# ====================== STYLESHEET (CSS) ======================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap');

:root {
    --red: #c83e3e;
    --red-dark: #a92f2f;
    --red-light: #fff5f5;
    --ink: #1f2937;
    --muted: #6b7280;
    --border: #e5e7eb;
    --surface: #ffffff;
    --bg: #f8fafc;
}

html, body, [class*="css"], input, button, textarea, [data-testid="stMarkdownContainer"] {
    font-family: 'Be Vietnam Pro', 'Segoe UI', Roboto, sans-serif !important;
}

.stApp {
    background: var(--bg);
    color: var(--ink);
}

header[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu, footer {
    visibility: hidden;
}

.block-container {
    max-width: 1300px;
    padding: 18px 24px 12px !important;
}

/* Header thương hiệu */
.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
}

.brand-icon {
    width: 44px;
    height: 44px;
    background: var(--red);
    color: white;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    font-weight: 800;
    box-shadow: 0 4px 10px rgba(200, 62, 62, 0.2);
}

.brand-name {
    font-size: 24px;
    font-weight: 800;
    color: var(--ink);
    line-height: 1.2;
}

.brand-subtitle {
    color: var(--muted);
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.5px;
    margin-top: 2px;
}

/* Tiêu đề mục */
.section-heading {
    font-size: 20px;
    font-weight: 700;
    color: var(--ink);
    margin: 0 0 4px;
}

.section-description {
    font-size: 13px;
    color: var(--muted);
    margin-bottom: 12px;
}

/* Căn giữa cột trái */
.left-col-header {
    text-align: center !important;
}

.left-col-header .section-heading,
.left-col-header .section-description {
    text-align: center !important;
}

/* Khung container nổi */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 16px 20px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.02);
}

/* Custom Khung Upload & Căn Giữa Cột */
div[data-testid="stFileUploader"] {
    width: 100% !important;
    display: flex !important;
    justify-content: center !important;
}

div[data-testid="stFileUploader"] section,
div[data-testid="stFileUploaderDropzone"] {
    background-color: var(--red-light) !important;
    border: 2px dashed #f0a3a3 !important;
    border-radius: 14px !important;
    padding: 24px 16px !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    width: 100% !important;
}

div[data-testid="stFileUploaderDropzone"] * {
    text-align: center !important;
}

div[data-testid="stFileUploaderDropzone"] > div {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    gap: 10px !important;
    width: 100% !important;
}

/* NÚT UPLOAD - MÀU ĐỎ CHỦ ĐẠO & CĂN GIỮA */
div[data-testid="stFileUploaderDropzone"] button,
div[data-testid="stFileUploaderDropzone"] [data-testid*="Button"],
div[data-testid="stFileUploader"] button {
    background-color: var(--red) !important;
    background: var(--red) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    border-radius: 8px !important;
    border: none !important;
    padding: 8px 28px !important;
    margin: 0 auto !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 0 2px 6px rgba(200, 62, 62, 0.25) !important;
    transition: all 0.2s ease !important;
}

div[data-testid="stFileUploaderDropzone"] button:hover,
div[data-testid="stFileUploaderDropzone"] [data-testid*="Button"]:hover,
div[data-testid="stFileUploader"] button:hover {
    background-color: var(--red-dark) !important;
    background: var(--red-dark) !important;
    color: #ffffff !important;
    box-shadow: 0 4px 10px rgba(169, 47, 47, 0.35) !important;
    cursor: pointer !important;
}

div[data-testid="stFileUploaderDropzone"] button *,
div[data-testid="stFileUploaderDropzone"] [data-testid*="Button"] * {
    color: #ffffff !important;
}

/* Chú thích phía dưới uploader */
.upload-caption-note {
    color: var(--muted);
    font-size: 13px;
    margin-top: 14px;
    text-align: center;
    font-weight: 500;
}

/* Radio button & Checkbox label */
div[data-testid="stRadio"] label p,
div[data-testid="stRadio"] p,
div[data-testid="stWidgetLabel"] p {
    font-size: 14px !important;
    font-weight: 600 !important;
    color: var(--ink) !important;
}

div[data-testid="stCheckbox"] label p {
    font-size: 14px !important;
    font-weight: 600 !important;
    color: var(--ink) !important;
}

/* Ghi chú hướng dẫn tùy chọn nâng cao */
.user-note {
    background: #f8fafc;
    border-left: 3px solid var(--red);
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 12px;
    color: #334155;
    line-height: 1.5;
    margin: 4px 0 12px 24px;
}

/* Dynamic Tip Box */
.tip-box {
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 13px;
    line-height: 1.5;
    margin: 8px 0 14px;
    transition: all 0.3s ease;
}

/* Nút bấm chung */
div.stButton > button,
div[data-testid="stDownloadButton"] button {
    background: var(--red) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    min-height: 42px !important;
    box-shadow: 0 3px 8px rgba(200, 62, 62, 0.2) !important;
}

div.stButton > button:hover,
div[data-testid="stDownloadButton"] button:hover {
    background: var(--red-dark) !important;
}

.preview-label {
    font-size: 16px;
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 8px;
}

.custom-divider {
    height: 1px;
    background-color: var(--border);
    margin: 16px 0;
}

.footer {
    text-align: center;
    color: var(--muted);
    font-size: 11px;
    padding: 20px 0 6px;
}
</style>
""", unsafe_allow_html=True)


# ====================== HEADER ======================
st.markdown("""
<div class="brand">
    <div class="brand-icon">S</div>
    <div>
        <div class="brand-name">ScanCare</div>
        <div class="brand-subtitle">SCAN DOCUMENT ENHANCEMENT</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ====================== TRANG 1: TẢI ẢNH & TÙY CHỌN ======================
if st.session_state.page == "upload":
    upload_col, options_col = st.columns([1.05, 0.95], gap="medium")

    with upload_col:
        st.markdown(
            '<div class="left-col-header">'
            '<div class="section-heading">01. Tải tài liệu lên</div>'
            '<div class="section-description">Chọn ảnh scan hoặc ảnh chụp cần cải thiện</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            uploaded_file = st.file_uploader(
                "Chọn ảnh",
                type=["jpg", "jpeg", "png"],
                label_visibility="collapsed",
                help="Hỗ trợ JPG, JPEG và PNG.",
            )

            if uploaded_file is not None:
                try:
                    img = Image.open(uploaded_file).convert("RGB")
                    st.session_state.image_original = img
                    st.session_state.file_name = uploaded_file.name

                    st.image(img, use_container_width=True)
                    st.caption(f"Ảnh đã chọn: {uploaded_file.name} | Kích thước: {img.size[0]} × {img.size[1]} px")
                except Exception:
                    st.session_state.image_original = None
                    st.error("Không thể đọc ảnh này. Vui lòng chọn ảnh JPG hoặc PNG khác.")
            else:
                st.session_state.image_original = None
                st.markdown(
                    '<div class="upload-caption-note">Vui lòng tải ảnh tài liệu lên để bắt đầu.</div>',
                    unsafe_allow_html=True,
                )

    with options_col:
        st.markdown(
            '<div class="section-heading">02. Tùy chọn xử lý</div>'
            '<div class="section-description">Chọn mức độ phù hợp với tình trạng tài liệu</div>',
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            st.markdown("**Hiển thị mức độ lọc nhiễu:**")

            st.session_state.noise_level = st.radio(
                "Mức lọc nhiễu",
                ["Nhẹ", "Vừa", "Mạnh"],
                index=["Nhẹ", "Vừa", "Mạnh"].index(st.session_state.noise_level),
                horizontal=True,
                label_visibility="collapsed",
            )

            # Lấy cấu hình màu sắc tương ứng với mức độ đã chọn
            current_tip = TIPS_CONFIG[st.session_state.noise_level]
            st.markdown(
                f'<div class="tip-box" style="{current_tip["style"]}">{current_tip["text"]}</div>',
                unsafe_allow_html=True,
            )

            st.markdown("**Tùy chọn nâng cao:**")
            
            st.session_state.enhance_contrast = st.checkbox(
                "Tăng độ tương phản",
                value=st.session_state.enhance_contrast,
            )
            st.markdown(
                '<div class="user-note">'
                '<b>Nên dùng khi:</b> Nền giấy bị tối/xám hoặc chữ bị nhạt màu. Tùy chọn này giúp chữ nổi bật và sắc nét hơn.'
                '</div>',
                unsafe_allow_html=True,
            )

            st.session_state.binarize = st.checkbox(
                "Làm rõ chữ bằng nhị phân hóa (Đen / Trắng)",
                value=st.session_state.binarize,
            )
            st.markdown(
                '<div class="user-note">'
                '<b>Nên dùng khi:</b> Tài liệu thuần văn bản trắng đen<br>'
                '<i>Không dùng khi: tài liệu có ảnh chụp, con dấu đỏ hoặc hình vẽ màu</i>'
                '</div>',
                unsafe_allow_html=True,
            )

            st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

            btn_process = st.button(
                "Nâng cao chất lượng tài liệu",
                use_container_width=True,
                disabled=st.session_state.image_original is None,
            )

            if btn_process and st.session_state.image_original is not None:
                st.session_state.image_processed = process_document(
                    st.session_state.image_original,
                    st.session_state.noise_level,
                    st.session_state.enhance_contrast,
                    st.session_state.binarize,
                )
                st.session_state.page = "result"
                st.rerun()


# ====================== TRANG 2: TRANG KẾT QUẢ & CẤU HÌNH LẠI ======================
elif st.session_state.page == "result":
    
    # HÀNG TRÊN CÙNG: Nút "Chọn ảnh khác" ở góc trái + Tiêu đề căn giữa 100%
    top_left, top_center, top_right = st.columns([1.5, 7, 1.5])

    with top_left:
        if st.button("← Chọn ảnh khác"):
            st.session_state.page = "upload"
            st.rerun()

    with top_center:
        st.markdown(
            '<div style="text-align: center; margin-bottom: 12px;">'
            '<div class="section-heading" style="font-size: 22px;">Kết quả nâng cao chất lượng</div>'
            '<div class="section-description" style="margin-bottom: 0;">Đối chiếu trực tiếp giữa ảnh gốc và ảnh đã qua xử lý</div>'
            '</div>',
            unsafe_allow_html=True,
        )

    # SO SÁNH 2 ẢNH
    col_orig, col_res = st.columns(2, gap="medium")

    with col_orig:
        st.markdown('<div class="preview-label">Ảnh gốc</div>', unsafe_allow_html=True)
        if st.session_state.image_original is not None:
            st.image(st.session_state.image_original, use_container_width=True)

    with col_res:
        st.markdown('<div class="preview-label">Ảnh đã chỉnh sửa</div>', unsafe_allow_html=True)
        if st.session_state.image_processed is not None:
            st.image(st.session_state.image_processed, use_container_width=True)

            img_bytes = image_to_bytes(st.session_state.image_processed)
            st.download_button(
                label="Tải ảnh kết quả về máy",
                data=img_bytes,
                file_name=f"enhanced_{st.session_state.file_name}",
                mime="image/png",
                use_container_width=True,
            )

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # KHUNG ĐIỀU CHỈNH VÀ XỬ LÝ LẠI
    st.markdown(
        '<div class="section-heading">Thay đổi tùy chọn & Xử lý lại</div>'
        '<div class="section-description">Đổi mức độ hoặc bật/tắt tùy chọn nâng cao bên dưới để thử kết quả mới</div>',
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        col_opt1, col_opt2 = st.columns(2, gap="medium")

        with col_opt1:
            st.markdown("**Thay đổi mức độ lọc nhiễu:**")
            st.session_state.noise_level = st.radio(
                "Mức độ lọc nhiễu (Kết quả)",
                ["Nhẹ", "Vừa", "Mạnh"],
                index=["Nhẹ", "Vừa", "Mạnh"].index(st.session_state.noise_level),
                horizontal=True,
                key="radio_result_page",
            )
            
            # Đổi màu chú thích tương ứng trên trang kết quả
            current_tip = TIPS_CONFIG[st.session_state.noise_level]
            st.markdown(
                f'<div class="tip-box" style="{current_tip["style"]}">{current_tip["text"]}</div>',
                unsafe_allow_html=True,
            )

        with col_opt2:
            st.markdown("**Tùy chọn nâng cao:**")
            st.session_state.enhance_contrast = st.checkbox(
                "Tăng độ tương phản",
                value=st.session_state.enhance_contrast,
                key="contrast_result_page",
            )
            st.markdown(
                '<div class="user-note"> Dùng khi chữ bị mờ hoặc nền xám.</div>',
                unsafe_allow_html=True,
            )

            st.session_state.binarize = st.checkbox(
                "Làm rõ chữ bằng nhị phân hóa",
                value=st.session_state.binarize,
                key="binarize_result_page",
            )
            st.markdown(
                '<div class="user-note"> Chỉ dùng cho tài liệu chữ trắng đen.</div>',
                unsafe_allow_html=True,
            )

        btn_reprocess = st.button("Nâng cao lại chất lượng", use_container_width=True)

        if btn_reprocess:
            st.session_state.image_processed = process_document(
                st.session_state.image_original,
                st.session_state.noise_level,
                st.session_state.enhance_contrast,
                st.session_state.binarize,
            )
            st.rerun()


# ====================== FOOTER ======================
st.markdown("""
<div class="footer">
    ScanCare | Nâng cao chất lượng tài liệu Scan
</div>
""", unsafe_allow_html=True)