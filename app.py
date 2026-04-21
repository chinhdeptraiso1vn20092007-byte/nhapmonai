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

# --- 2. CẤU HÌNH AI THÔNG MINH CHỐNG NGHẼN ---
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("🔑 Thiếu API Key trong Secrets!")
    st.stop()

genai.configure(api_key=api_key)

def call_ai_25(content):
    """Chiến thuật tự động thử lại khi gặp lỗi quá tải băng thông"""
    max_retries = 3  # Thử lại tối đa 3 lần
    
    # Lấy danh sách model khả dụng một lần để tránh gọi liên tục
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Ưu tiên Flash vì hạn mức cao nhất
        target_model = next((m for m in ['models/gemini-1.5-flash', 'models/gemini-pro'] if m in available_models), available_models[0])
    except:
        target_model = 'gemini-1.5-flash' # Fallback mặc định

    for attempt in range(max_retries):
        try:
            model = genai.GenerativeModel(target_model)
            response = model.generate_content(f"Bạn là chuyên gia Văn Hiến AI 2.5. Xử lý yêu cầu: {content}")
            return response.text
        except Exception as e:
            err_str = str(e)
            # Nếu lỗi 429 (Quá tải)
            if "429" in err_str or "ResourceExhausted" in err_str:
                if attempt < max_retries - 1:
                    # Đợi tăng dần: 2s, 4s, 8s cộng thêm chút ngẫu nhiên
                    wait_time = (2 ** (attempt + 1)) + random.random()
                    time.sleep(wait_time)
                    continue
                return "🚀 Máy chủ Google đang quá tải nghiêm trọng. Bạn hãy nghỉ tay khoảng 30 giây rồi thử lại nhé!"
            return f"❌ Lỗi: {err_str}"

# --- 3. GIAO DIỆN CHÍNH ---
st.markdown("<h1 class='main-title'>VĂN HIẾN AI 2.5</h1>", unsafe_allow_html=True)

tabs = st.tabs(["📝 DÀN Ý", "🎓 CHẤM ĐIỂM", "📡 DẪN CHỨNG"])

with tabs[0]:
    p1 = st.text_area("Nhập đề bài:", height=120, key="t1")
    if st.button("LẬP DÀN Ý 2.5", key="b1"):
        if p1:
            with st.spinner("AI 2.5 đang tính toán..."):
                res = call_ai_25(f"Lập dàn ý chi tiết: {p1}")
                st.markdown(f"<div class='result-card'>{res}</div>", unsafe_allow_html=True)

with tabs[1]:
    p2 = st.text_area("Dán bài làm:", height=200, key="t2")
    if st.button("CHẤM ĐIỂM 2.5", key="b2"):
        if p2:
            with st.spinner("AI 2.5 đang thẩm định..."):
                res = call_ai_25(f"Chấm điểm và nhận xét: {p2}")
                st.markdown(f"<div class='result-card'>{res}</div>", unsafe_allow_html=True)

with tabs[2]:
    p3 = st.text_input("Vấn đề xã hội:", key="t3")
    if st.button("TÌM DẪN CHỨNG 2.5", key="b3"):
        if p3:
            with st.spinner("AI 2.5 đang tra cứu..."):
                res = call_ai_25(f"Dẫn chứng mới nhất về: {p3}")
                st.markdown(f"<div class='result-card'>{res}</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("Bản cập nhật ổn định hóa băng thông 2.5 • 2026")
