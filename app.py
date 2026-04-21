import streamlit as st
import google.generativeai as genai
import time

# --- 1. GIAO DIỆN VĂN HIẾN AI 2.5 ---
st.set_page_config(page_title="VĂN HIẾN AI 2.5", page_icon="💎")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    p, span, h1, h2, h3 { color: #000000 !important; font-weight: 800 !important; }
    .main-title { color: #e11d48 !important; text-align: center; font-size: 3rem !important; font-weight: 900 !important; }
    .stButton>button {
        width: 100%; background: #e11d48 !important; color: white !important;
        font-weight: 900 !important; height: 60px; border-radius: 12px !important;
    }
    .result-card {
        background: #f8fafc; padding: 20px; border-radius: 12px;
        border-left: 10px solid #e11d48; color: #000000 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-top: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CẤU HÌNH AI "LÌ ĐÒN" ---
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("🔑 Chưa nhập API Key!")
    st.stop()

genai.configure(api_key=api_key)

def call_ai_power(content):
    # CHÌA KHÓA: Đổi sang 1.5-flash để lấy hạn mức cao nhất (15 req/min)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    for i in range(5): # Thử lại 5 lần tự động
        try:
            response = model.generate_content(f"Bạn là Văn Hiến AI 2.5. Hãy xử lý: {content}")
            return response.text
        except Exception as e:
            if "429" in str(e):
                # Nếu bị bóp băng thông, đợi lâu hơn một chút (3-5 giây)
                time.sleep(4)
                continue
            return f"❌ Lỗi: {str(e)}"
    return "⚠️ Google đang quá tải. Bạn hãy đợi khoảng 15 giây rồi thử lại nhé!"

# --- 3. GIAO DIỆN ---
st.markdown("<h1 class='main-title'>VĂN HIẾN AI 2.5</h1>", unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["📝 DÀN Ý", "🎓 CHẤM ĐIỂM", "📡 DẪN CHỨNG"])

with t1:
    p1 = st.text_area("Đề bài:", key="p1")
    if st.button("XỬ LÝ DÀN Ý 2.5"):
        if p1:
            with st.spinner("AI 2.5 đang xử lý..."):
                st.markdown(f"<div class='result-card'>{call_ai_power(f'Lập dàn ý: {p1}')}</div>", unsafe_allow_html=True)

with t2:
    p2 = st.text_area("Bài làm:", key="p2", height=200)
    if st.button("THẨM ĐỊNH BÀI 2.5"):
        if p2:
            with st.spinner("AI 2.5 đang chấm bài..."):
                st.markdown(f"<div class='result-card'>{call_ai_power(f'Chấm điểm: {p2}')}</div>", unsafe_allow_html=True)

with t3:
    p3 = st.text_input("Vấn đề:", key="p3")
    if st.button("TÌM DẪN CHỨNG 2.5"):
        if p3:
            with st.spinner("AI 2.5 đang tìm..."):
                st.markdown(f"<div class='result-card'>{call_ai_power(f'Dẫn chứng: {p3}')}</div>", unsafe_allow_html=True)
