import streamlit as st
import google.generativeai as genai
import time

# --- GIAO DIỆN SIÊU TƯƠNG PHẢN ---
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
if "GEMINI_API_KEY" not in st.secrets:
    st.error("🔑 Thiếu API Key trong Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def call_ai_25(content):
    """Hàm gọi AI thông minh tự động tránh lỗi 404"""
    # Thử các định danh model phổ biến nhất
    for m_name in ['gemini-1.5-flash', 'models/gemini-1.5-flash', 'gemini-pro']:
        try:
            model = genai.GenerativeModel(m_name)
            response = model.generate_content(f"Hệ thống Văn Hiến AI 2.5 xử lý chuyên sâu: {content}")
            return response.text
        except:
            continue
    return "⚠️ Hiện tại tất cả các cổng kết nối AI đều bận hoặc không tìm thấy model phù hợp. Vui lòng thử lại sau 30 giây."

# --- GIAO DIỆN CHÍNH ---
st.markdown("<h1 class='main-title'>VĂN HIẾN AI 2.5</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #e11d48 !important;'>Cấu trúc mô hình 2.5 hoàn chỉnh</p>", unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["📝 DÀN Ý", "🎓 CHẤM ĐIỂM", "📡 DẪN CHỨNG"])

with t1:
    p1 = st.text_area("Nhập đề bài văn học:", height=120, key="t1")
    if st.button("LẬP DÀN Ý 2.5", key="b1"):
        if p1:
            with st.spinner("AI 2.5 đang lập dàn ý..."):
                res = call_ai_25(f"Lập dàn ý chi tiết: {p1}")
                st.markdown(f"<div class='result-card'>{res}</div>", unsafe_allow_html=True)

with t2:
    p2 = st.text_area("Dán bài làm của học sinh:", height=200, key="t2")
    if st.button("CHẤM ĐIỂM 2.5", key="b2"):
        if p2:
            with st.spinner("AI 2.5 đang thẩm định..."):
                res = call_ai_25(f"Chấm điểm và nhận xét bài văn: {p2}")
                st.markdown(f"<div class='result-card'>{res}</div>", unsafe_allow_html=True)

with t3:
    p3 = st.text_input("Vấn đề xã hội:", key="t3")
    if st.button("TÌM DẪN CHỨNG 2.5", key="b3"):
        if p3:
            with st.spinner("AI 2.5 đang tra cứu..."):
                res = call_ai_25(f"Tìm dẫn chứng thời sự về: {p3}")
                st.markdown(f"<div class='result-card'>{res}</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("Phiên bản cấu trúc mô hình 2.5 - Tối ưu kết nối API • 2026")
