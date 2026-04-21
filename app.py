import streamlit as st
import google.generativeai as genai
import time

# --- 1. CẤU HÌNH GIAO DIỆN SIÊU TƯƠNG PHẢN ---
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
    }
    .result-card {
        background: #ffffff; padding: 25px; border-radius: 15px;
        border: 4px solid #e11d48; color: #000000 !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CẤU HÌNH MÔ HÌNH 2.5 ---
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("🔑 Thiếu API Key trong phần Secrets!")
    st.stop()

genai.configure(api_key=api_key)

def call_ai_power(content):
    """Sử dụng cấu trúc mô hình 2.5 theo yêu cầu"""
    try:
        # Cấu hình gọi đúng model 2.5 Flash
        # Lưu ý: Nếu Google báo lỗi 404, hãy đổi lại thành 'gemini-1.5-flash-latest'
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        res = model.generate_content(f"Hệ thống Văn Hiến AI 2.5 xử lý: {content}")
        return res.text
    except Exception as e:
        # Xử lý lỗi quota hoặc model chưa khả dụng
        if "404" in str(e):
            return "❌ Lỗi 404: Model 2.5 Flash hiện chưa được Google mở cổng API chính thức tại vùng này. Hãy thử lại với bản 1.5 Flash."
        if "429" in str(e):
            time.sleep(5)
            return "⚠️ Hệ thống đang bận, vui lòng thử lại sau vài giây."
        return f"❌ Lỗi: {str(e)}"

# --- 3. GIAO DIỆN CHÍNH ---
st.markdown("<h1 class='main-title'>VĂN HIẾN AI 2.5</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #e11d48 !important; font-weight: bold;'>Cấu trúc mô hình 2.5 hoàn chỉnh</p>", unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["📝 DÀN Ý", "🕵️ CHẤM ĐIỂM", "📡 DẪN CHỨNG"])

with t1:
    p1 = st.text_area("Nhập đề bài:", height=120, key="t1")
    if st.button("LẬP DÀN Ý 2.5", key="b1"):
        if p1:
            with st.spinner("AI 2.5 đang lập dàn ý..."):
                res = call_ai_power(f"Lập dàn ý chi tiết bài văn: {p1}")
                st.markdown(f"<div class='result-card'>{res}</div>", unsafe_allow_html=True)

with t2:
    p2 = st.text_area("Dán bài làm:", height=200, key="t2")
    if st.button("CHẤM ĐIỂM 2.5", key="b2"):
        if p2:
            with st.spinner("AI 2.5 đang chấm bài..."):
                res = call_ai_power(f"Chấm điểm và nhận xét bài văn: {p2}")
                st.markdown(f"<div class='result-card'>{res}</div>", unsafe_allow_html=True)

with t3:
    p3 = st.text_input("Vấn đề xã hội:", key="t3")
    if st.button("TÌM DẪN CHỨNG 2.5", key="b3"):
        if p3:
            with st.spinner("AI 2.5 đang tìm dẫn chứng..."):
                res = call_ai_power(f"Dẫn chứng thời sự về: {p3}")
                st.markdown(f"<div class='result-card'>{res}</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("Phiên bản cấu trúc mô hình 2.5 sạch mã nguồn • 2026")
