import streamlit as st
import google.generativeai as genai
import time

# --- GIAO DIỆN SIÊU TƯƠNG PHẢN ---
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
        font-weight: 900 !important; height: 65px; border-radius: 15px !important;
        font-size: 1.3rem !important; border: none !important;
    }
    .result-card {
        background: #ffffff; padding: 25px; border-radius: 15px;
        border: 4px solid #e11d48; color: #000000 !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1); margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CẤU HÌNH AI NÂNG CAO ---
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("🔑 Thiếu API Key trong Secrets!")
    st.stop()

genai.configure(api_key=api_key)

def call_ai_25(content):
    """Cấu trúc tự phục hồi: Thử lại khi quá tải và tự chọn Model"""
    max_retries = 2  # Thử lại tối đa 2 lần nếu lỗi
    
    for attempt in range(max_retries + 1):
        try:
            # 1. Tìm model khả dụng nhất
            available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            target = next((m for m in ['models/gemini-1.5-flash', 'models/gemini-pro'] if m in available), available[0])
            
            # 2. Gọi model
            model = genai.GenerativeModel(target)
            response = model.generate_content(f"Bạn là chuyên gia Văn Hiến AI 2.5. Xử lý: {content}")
            return response.text

        except Exception as e:
            if "429" in str(e) and attempt < max_retries:
                time.sleep(3)  # Nghỉ ngắn 3 giây trước khi thử lại tự động
                continue
            return f"⚠️ Hệ thống đang rất bận. Bạn vui lòng đợi khoảng 15 giây rồi hãy bấm nút lần nữa nhé!"

# --- GIAO DIỆN CHÍNH ---
st.markdown("<h1 class='main-title'>VĂN HIẾN AI 2.5</h1>", unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["📝 DÀN Ý", "🎓 CHẤM ĐIỂM", "📡 DẪN CHỨNG"])

with t1:
    p1 = st.text_area("Nhập đề bài văn học:", height=120, key="t1")
    if st.button("LẬP DÀN Ý 2.5", key="b1"):
        if p1:
            with st.spinner("AI 2.5 đang phân tích..."):
                st.markdown(f"<div class='result-card'>{call_ai_25(f'Lập dàn ý chi tiết: {p1}')}</div>", unsafe_allow_html=True)

with t2:
    p2 = st.text_area("Dán bài làm của học sinh:", height=200, key="t2")
    if st.button("CHẤM ĐIỂM 2.5", key="b2"):
        if p2:
            with st.spinner("AI 2.5 đang thẩm định..."):
                st.markdown(f"<div class='result-card'>{call_ai_25(f'Chấm điểm và nhận xét: {p2}')}</div>", unsafe_allow_html=True)

with t3:
    p3 = st.text_input("Vấn đề xã hội:", key="t3")
    if st.button("TÌM DẪN CHỨNG 2.5", key="b3"):
        if p3:
            with st.spinner("AI 2.5 đang tra cứu..."):
                st.markdown(f"<div class='result-card'>{call_ai_25(f'Dẫn chứng thời sự về: {p3}')}</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("Bản cập nhật ổn định hóa băng thông mô hình 2.5 • 2026")
