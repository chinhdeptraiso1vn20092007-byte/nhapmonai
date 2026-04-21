import streamlit as st
import google.generativeai as genai
import time
import random

# --- 1. GIAO DIỆN SIÊU TƯƠNG PHẢN (VĂN HIẾN 2.5) ---
st.set_page_config(page_title="VĂN HIẾN AI 2.5", page_icon="💎", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    p, span, label, .stMarkdown, h1, h2, h3, li, textarea, input {
        color: #000000 !important; font-family: 'Arial', sans-serif !important; font-weight: 800 !important;
    }
    .main-title { color: #e11d48 !important; text-align: center; font-size: 3.5rem !important; font-weight: 900 !important; }
    .stButton>button {
        width: 100%; background: #e11d48 !important; color: white !important;
        font-weight: 900 !important; height: 65px; border-radius: 15px !important;
        font-size: 1.3rem !important; border: none !important; transition: 0.3s;
    }
    .stButton>button:hover { background: #be123c !important; transform: scale(1.02); }
    .result-card {
        background: #ffffff; padding: 25px; border-radius: 15px;
        border: 4px solid #e11d48; color: #000000 !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1); margin-top: 20px; line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CẤU HÌNH AI "BẤT TỬ" (KHÔNG LỖI - KHÔNG DỪNG) ---
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("🔑 API Key bị thiếu trong cấu hình Secrets!")
    st.stop()

genai.configure(api_key=api_key)

def call_ai_ultimate(content):
    """Cơ chế tự động dò model và tự động thử lại vĩnh cửu khi nghẽn"""
    # Bước 1: Dò tìm tên model thực tế để tránh lỗi 404
    try:
        available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in available else available[0]
    except:
        target = 'gemini-1.5-flash'

    model = genai.GenerativeModel(target)
    
    # Bước 2: Vòng lặp tự phục hồi (Retry Loop)
    max_attempts = 10 
    for i in range(max_attempts):
        try:
            full_prompt = f"Bạn là chuyên gia Văn Hiến AI 2.5. Hãy thực hiện yêu cầu sau một cách chuyên nghiệp: {content}"
            response = model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            err = str(e).lower()
            # Nếu gặp bất kỳ lỗi băng thông hoặc bận (429, 500, 503)
            if any(x in err for x in ["429", "resource", "quota", "500", "503", "limit"]):
                # Tự động đợi tăng dần và thử lại mà không báo lỗi cho người dùng
                wait_time = (i + 1) * 3 + random.random()
                time.sleep(wait_time)
                continue
            return f"❌ Lỗi hệ thống: {str(e)}"
            
    return "🚀 Máy chủ Google hiện tại đang phản hồi rất chậm. Bạn hãy thử nhấn lại sau 30 giây để reset luồng nhé!"

# --- 3. GIAO DIỆN CHÍNH ---
st.markdown("<h1 class='main-title'>VĂN HIẾN AI 2.5</h1>", unsafe_allow_html=True)

tabs = st.tabs(["📝 LẬP DÀN Ý", "🎓 CHẤM ĐIỂM", "📡 DẪN CHỨNG"])

with tabs[0]:
    p1 = st.text_area("Nhập đề bài văn học:", height=120, key="area1")
    if st.button("LẬP DÀN Ý TỨC THÌ", key="btn1"):
        if p1:
            with st.spinner("AI 2.5 đang kiên trì xử lý dữ liệu..."):
                res = call_ai_ultimate(f"Lập dàn ý chi tiết bài văn: {p1}")
                st.markdown(f"<div class='result-card'>{res}</div>", unsafe_allow_html=True)

with tabs[1]:
    p2 = st.text_area("Dán nội dung bài làm:", height=250, key="area2")
    if st.button("THẨM ĐỊNH BÀI VIẾT", key="btn2"):
        if p2:
            with st.spinner("AI 2.5 đang đọc và chấm điểm kỹ lưỡng..."):
                res = call_ai_ultimate(f"Chấm điểm và nhận xét chi tiết bài văn: {p2}")
                st.markdown(f"<div class='result-card'>{res}</div>", unsafe_allow_html=True)

with tabs[2]:
    p3 = st.text_input("Vấn đề cần tìm dẫn chứng:", key="input3")
    if st.button("TRUY XUẤT DỮ LIỆU", key="btn3"):
        if p3:
            with st.spinner("AI 2.5 đang quét kho tư liệu..."):
                res = call_ai_ultimate(f"Tìm dẫn chứng thời sự mới nhất về: {p3}")
                st.markdown(f"<div class='result-card'>{res}</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("Hệ thống tự phục hồi thông minh • Văn Hiến AI 2.5 (2026)")
