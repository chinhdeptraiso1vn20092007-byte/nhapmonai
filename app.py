import streamlit as st
import google.generativeai as genai
import time

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="VĂN HIẾN AI 2.5", page_icon="💎", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    p, span, label, .stMarkdown, h1, h2, h3, li, textarea, input {
        color: #000000 !important; 
        font-family: 'Arial', sans-serif !important;
        font-weight: 800 !important;
    }
    .main-title { 
        color: #e11d48 !important; 
        text-align: center; 
        font-size: 3rem !important; 
        font-weight: 900 !important;
    }
    .stButton>button {
        width: 100%; background: #e11d48 !important; color: white !important;
        font-weight: 900 !important; height: 65px; border-radius: 15px !important;
        font-size: 1.3rem !important; border: none !important;
    }
    .result-card {
        background: #ffffff; padding: 25px; border-radius: 15px;
        border: 4px solid #e11d48; color: #000000 !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CẤU HÌNH AI ---
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("🔑 Thiếu API Key!")
    st.stop()

genai.configure(api_key=api_key)

def call_ai_power(content):
    try:
        # TÊN MODEL ĐÃ ĐƯỢC SỬA ĐỂ TRÁNH LỖI 404
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        res = model.generate_content(f"Bạn là chuyên gia Văn học 2.5. Xử lý: {content}")
        return res.text
    except Exception as e:
        if "429" in str(e):
            return "⚠️ Hệ thống đang bận, vui lòng đợi 10 giây rồi thử lại."
        return f"❌ Lỗi hệ thống: {str(e)}"

# --- GIAO DIỆN ---
st.markdown("<h1 class='main-title'>VĂN HIẾN AI 2.5</h1>", unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["📝 DÀN Ý", "🎓 CHẤM ĐIỂM", "📡 DẪN CHỨNG"])

with t1:
    p1 = st.text_area("Nhập đề bài:", height=120, key="t1")
    if st.button("LẬP DÀN Ý 2.5", key="b1"):
        if p1:
            with st.spinner("Đang xử lý..."):
                res = call_ai_power(f"Lập dàn ý: {p1}")
                st.markdown(f"<div class='result-card'>{res}</div>", unsafe_allow_html=True)

with t2:
    p2 = st.text_area("Dán bài làm:", height=200, key="t2")
    if st.button("CHẤM ĐIỂM 2.5", key="b2"):
        if p2:
            with st.spinner("Đang chấm bài..."):
                res = call_ai_power(f"Chấm điểm bài văn: {p2}")
                st.markdown(f"<div class='result-card'>{res}</div>", unsafe_allow_html=True)

with t3:
    p3 = st.text_input("Vấn đề xã hội:", key="t3")
    if st.button("TÌM DẪN CHỨNG 2.5", key="b3"):
        if p3:
            with st.spinner("Đang tìm..."):
                res = call_ai_power(f"Tìm dẫn chứng về: {p3}")
                st.markdown(f"<div class='result-card'>{res}</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("Phiên bản sửa lỗi kết nối Model • 2026")
