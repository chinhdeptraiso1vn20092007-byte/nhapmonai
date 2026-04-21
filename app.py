import streamlit as st
import google.generativeai as genai
import time

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

# --- 2. ĐỘNG CƠ TỰ ĐỘNG CẤU HÌNH (CHỐNG LỖI 100%) ---
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("🔑 Chưa cấu hình GEMINI_API_KEY!")
    st.stop()

genai.configure(api_key=api_key)

def call_ai_power(content):
    """Tự động dò tìm model khả dụng để xử lý"""
    try:
        # Bước 1: Liệt kê các model mà API Key này được phép dùng
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Bước 2: Chọn model theo thứ tự ưu tiên (Flash -> Pro)
        selected_model = None
        for target in ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']:
            if target in available_models:
                selected_model = target
                break
        
        if not selected_model:
            selected_model = available_models[0] # Lấy model đầu tiên nếu không thấy cái ưu tiên

        # Bước 3: Thực hiện lệnh
        model = genai.GenerativeModel(selected_model)
        full_prompt = f"Bạn là chuyên gia Văn Hiến AI 2.5. Hãy xử lý: {content}"
        response = model.generate_content(full_prompt)
        return response.text

    except Exception as e:
        err_msg = str(e).lower()
        if "429" in err_msg or "resource" in err_msg:
            return "⚠️ **Băng thông đang reset.** Bạn đợi 5-10 giây rồi nhấn lại nút nhé. AI 2.5 sẽ phản hồi ngay!"
        return f"❌ Lỗi: {str(e)}"

# --- 3. GIAO DIỆN CHÍNH ---
st.markdown("<h1 class='main-title'>VĂN HIẾN AI 2.5</h1>", unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["📝 LẬP DÀN Ý", "🎓 CHẤM ĐIỂM", "📡 DẪN CHỨNG"])

with t1:
    p1 = st.text_area("Nhập đề bài:", key="p1", height=100)
    if st.button("XỬ LÝ DÀN Ý 2.5"):
        if p1:
            with st.spinner("AI 2.5 đang làm việc..."):
                st.markdown(f"<div class='result-card'>{call_ai_power(f'Lập dàn ý: {p1}')}</div>", unsafe_allow_html=True)

with t2:
    p2 = st.text_area("Dán bài làm:", key="p2", height=200)
    if st.button("THẨM ĐỊNH BÀI 2.5"):
        if p2:
            with st.spinner("AI 2.5 đang chấm điểm..."):
                st.markdown(f"<div class='result-card'>{call_ai_power(f'Chấm điểm bài: {p2}')}</div>", unsafe_allow_html=True)

with t3:
    p3 = st.text_input("Vấn đề cần dẫn chứng:", key="p3")
    if st.button("TÌM DẪN CHỨNG 2.5"):
        if p3:
            with st.spinner("AI 2.5 đang tra cứu..."):
                st.markdown(f"<div class='result-card'>{call_ai_power(f'Tìm dẫn chứng về: {p3}')}</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("© 2026 Văn Hiến AI - Cấu trúc tự sửa lỗi nâng cao")
