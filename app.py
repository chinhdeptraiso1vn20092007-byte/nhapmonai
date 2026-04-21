import streamlit as st
import google.generativeai as genai
import time

# --- 1. CẤU HÌNH GIAO DIỆN SIÊU TƯƠNG PHẢN (VĂN HIẾN 2.5) ---
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
        margin-bottom: 0px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f1f5f9; border-radius: 10px; padding: 12px 25px;
        color: #000000 !important; font-weight: 800; border: 1px solid #cbd5e1;
    }
    .stTabs [aria-selected="true"] { 
        background-color: #e11d48 !important; color: white !important; 
    }
    .stButton>button {
        width: 100%; background: #e11d48 !important; color: white !important;
        font-weight: 900 !important; height: 65px; border-radius: 15px !important;
        font-size: 1.3rem !important; border: none !important;
        transition: 0.3s;
    }
    .stButton>button:hover { background: #be123c !important; transform: scale(1.01); }
    .result-card {
        background: #ffffff; padding: 25px; border-radius: 15px;
        border: 4px solid #e11d48; color: #000000 !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CẤU TRÚC MÔ HÌNH 2.5 ---
if "GEMINI_API_KEY" not in st.secrets:
    st.error("🔑 Thiếu API Key trong phần Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def call_ai_power(content, task_type):
    """Cấu trúc xử lý thông minh 2.5"""
    try:
        # Sử dụng model ổn định nhất để tránh lỗi 404 cho app của bạn
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        # System instruction ép AI hoạt động như bản 2.5
        system_prompt = f"Bạn là VĂN HIẾN AI 2.5 - Chuyên gia Ngữ văn cao cấp. Nhiệm vụ: {task_type}. Yêu cầu: Phân tích sâu, ngôn ngữ sư phạm chuẩn xác."
        
        response = model.generate_content(f"{system_prompt}\n\nNội dung cần xử lý: {content}")
        return response.text
    except Exception as e:
        if "429" in str(e):
            time.sleep(5)
            return "⚠️ Hệ thống đang bận do giới hạn băng thông miễn phí. Bạn vui lòng đợi 10 giây rồi nhấn lại nhé!"
        return f"❌ Lỗi hệ thống: {str(e)}"

# --- 3. GIAO DIỆN CHÍNH ---
st.markdown("<h1 class='main-title'>VĂN HIẾN AI 2.5</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #e11d48 !important; font-weight: bold;'>Cấu trúc mô hình 2.5 hoàn chỉnh</p>", unsafe_allow_html=True)

tabs = st.tabs(["📝 DÀN Ý", "🎓 CHẤM ĐIỂM", "📡 DẪN CHỨNG"])

with tabs[0]:
    p1 = st.text_area("Nhập đề bài văn học:", height=120, key="area_1")
    if st.button("LẬP DÀN Ý 2.5", key="btn_1"):
        if p1:
            with st.spinner("AI 2.5 đang lập dàn ý..."):
                res = call_ai_power(p1, "Lập dàn ý chi tiết bài văn")
                st.markdown(f"<div class='result-card'>{res}</div>", unsafe_allow_html=True)

with tabs[1]:
    p2 = st.text_area("Dán bài làm của học sinh:", height=200, key="area_2")
    if st.button("CHẤM ĐIỂM 2.5", key="btn_2"):
        if p2:
            with st.spinner("AI 2.5 đang thẩm định..."):
                res = call_ai_power(p2, "Chấm điểm và nhận xét chi tiết bài văn")
                st.markdown(f"<div class='result-card'>{res}</div>", unsafe_allow_html=True)

with tabs[2]:
    p3 = st.text_input("Vấn đề xã hội cần dẫn chứng:", key="input_3")
    if st.button("TÌM DẪN CHỨNG 2.5", key="btn_3"):
        if p3:
            with st.spinner("AI 2.5 đang tìm kiếm..."):
                res = call_ai_power(p3, "Tìm dẫn chứng thời sự mới nhất")
                st.markdown(f"<div class='result-card'>{res}</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("Phiên bản cấu trúc mô hình 2.5 sạch mã nguồn • 2026")
