import streamlit as st
import google.generativeai as genai
import time

# --- 1. GIAO DIỆN SIÊU TƯƠNG PHẢN ---
st.set_page_config(page_title="VĂN HIẾN AI 2.5", page_icon="💎", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    p, span, label, .stMarkdown, h1, h2, h3, li, textarea, input {
        color: #000000 !important; font-family: 'Arial', sans-serif !important; font-weight: 800 !important;
    }
    .main-title { color: #e11d48 !important; text-align: center; font-size: 3rem !important; font-weight: 900 !important; }
    .stButton>button {
        width: 100%; background: #e11d48 !important; color: white !important;
        font-weight: 900 !important; height: 60px; border-radius: 12px !important;
        font-size: 1.2rem !important; border: none !important;
    }
    .result-card {
        background: #ffffff; padding: 20px; border-radius: 12px;
        border: 3px solid #e11d48; color: #000000 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-top: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ĐỘNG CƠ VĂN HIẾN AI 2.5 (CHẮC CHẮN CHẠY) ---
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("🔑 Lỗi: Chưa tìm thấy GEMINI_API_KEY trong mục Secrets của Streamlit.")
    st.stop()

genai.configure(api_key=api_key)

def call_ai_power(content):
    # Sử dụng model phổ biến nhất để tuyệt đối không lỗi 404
    # Ghi rõ models/gemini-1.5-flash để hệ thống nhận diện tốt nhất
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        # Thêm tiền tố định danh cho hệ thống 2.5
        full_prompt = f"Bạn là hệ thống chuyên gia Văn Hiến AI 2.5. Hãy thực hiện: {content}"
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        err_msg = str(e).lower()
        if "429" in err_msg or "resource" in err_msg:
            return "⚠️ **Hệ thống đang xử lý hàng đợi.** Bạn vui lòng đợi 10 giây rồi nhấn lại nút để nhận kết quả nhé! Google cần một chút thời gian để reset băng thông cho gói miễn phí."
        elif "404" in err_msg:
            # Fallback sang model khác nếu 1.5 flash không tồn tại ở vùng đó
            try:
                alt_model = genai.GenerativeModel('gemini-pro')
                return alt_model.generate_content(content).text
            except:
                return "❌ Model hiện tại đang bảo trì. Bạn hãy thử lại sau ít phút."
        return f"❌ Thông báo: {str(e)}"

# --- 3. GIAO DIỆN NGƯỜI DÙNG ---
st.markdown("<h1 class='main-title'>VĂN HIẾN AI 2.5</h1>", unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["📝 LẬP DÀN Ý", "🎓 CHẤM ĐIỂM", "📡 DẪN CHỨNG"])

with t1:
    p1 = st.text_area("Nhập đề bài văn học:", key="p1", height=120)
    if st.button("XỬ LÝ DÀN Ý 2.5", key="b1"):
        if p1:
            with st.spinner("Đang kết nối AI 2.5..."):
                res = call_ai_power(f"Lập dàn ý chi tiết: {p1}")
                st.markdown(f"<div class='result-card'>{res}</div>", unsafe_allow_html=True)

with t2:
    p2 = st.text_area("Dán bài văn làm của học sinh:", key="p2", height=200)
    if st.button("THẨM ĐỊNH CHI TIẾT 2.5", key="b2"):
        if p2:
            with st.spinner("Đang chấm điểm chuyên sâu..."):
                res = call_ai_power(f"Chấm điểm và nhận xét ưu nhược điểm: {p2}")
                st.markdown(f"<div class='result-card'>{res}</div>", unsafe_allow_html=True)

with t3:
    p3 = st.text_input("Vấn đề xã hội cần dẫn chứng:", key="p3")
    if st.button("QUÉT DỮ LIỆU 2.5", key="b3"):
        if p3:
            with st.spinner("Đang tìm dẫn chứng..."):
                res = call_ai_power(f"Tìm 3 dẫn chứng mới nhất về: {p3}")
                st.markdown(f"<div class='result-card'>{res}</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("© 2026 Văn Hiến AI - Phiên bản 2.5 Hệ thống Siêu tốc")
