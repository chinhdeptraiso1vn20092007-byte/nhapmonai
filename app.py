import streamlit as st
import google.generativeai as genai
import time
import random

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

# --- CẤU HÌNH AI CHỐNG NGHẼN ---
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("🔑 Thiếu API Key trong Secrets!")
    st.stop()

genai.configure(api_key=api_key)

def call_ai_25(content):
    """Chiến thuật chống nghẽn: Tự động thử lại với thời gian giãn cách tăng dần"""
    # Danh sách model có hạn mức cao nhất cho gói Free
    models_to_try = ['models/gemini-1.5-flash', 'models/gemini-pro']
    
    max_retries = 3 
    for attempt in range(max_retries):
        try:
            # Tự động liệt kê và chọn model khả dụng
            model_name = models_to_try[attempt % len(models_to_try)]
            model = genai.GenerativeModel(model_name)
            
            response = model.generate_content(f"Hệ thống Văn Hiến AI 2.5 xử lý: {content}")
            return response.text

        except Exception as e:
            err_msg = str(e)
            # Nếu gặp lỗi Quá tải (429)
            if "429" in err_msg or "ResourceExhausted" in err_msg:
                # Đợi theo cấp số nhân + một chút ngẫu nhiên để tránh xung đột
                wait_time = (2 ** attempt) + random.random() 
                time.sleep(wait_time)
                continue 
            return f"❌ Lỗi: {err_msg}"
            
    return "🚀 Máy chủ Google đang quá tải nghiêm trọng. Bạn hãy nghỉ tay 30 giây rồi thử lại nhé!"

# --- GIAO DIỆN CHÍNH ---
st.markdown("<h1 class='main-title'>VĂN HIẾN AI 2.5</h1>", unsafe_allow_html=True)

tabs = st.tabs(["📝 DÀN Ý", "🎓 CHẤM ĐIỂM", "📡 DẪN CHỨNG"])

with tabs[0]:
    p1 = st.text_area("Nhập đề bài:", height=120, key="t1")
    if st.button("LẬP DÀN Ý 2.5", key="b1"):
        if p1:
            with st.spinner("AI 2.5 đang tính toán..."):
                st.markdown(f"<div class='result-card'>{call_ai_25(f'Lập dàn ý: {p1}')}</div>", unsafe_allow_html=True)

with tabs[1]:
    p2 = st.text_area("Dán bài làm:", height=200, key="t2")
    if st.button("CHẤM ĐIỂM 2.5", key="b2"):
        if p2:
            with st.spinner("AI 2.5 đang thẩm định..."):
                st.markdown(f"<div class='result-card'>{call_ai_25(f'Chấm điểm: {p2}')}</div>", unsafe_allow_html=True)

with tabs[2]:
    p3 = st.text_input("Vấn đề xã hội:", key="t3")
    if st.button("TÌM DẪN CHỨNG 2.5", key="b3"):
        if p3:
            with st.spinner("AI 2.5 đang tra cứu..."):
                st.markdown(f"<div class='result-card'>{call_ai_25(f'Dẫn chứng: {p3}')}</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("Bản cập nhật ổn định hóa 2.5 - Chống nghẽn API • 2026")
