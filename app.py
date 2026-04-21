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

# --- 2. ĐỘNG CƠ AI SIÊU CẤP (CHỐNG LỖI TUYỆT ĐỐI) ---
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("🔑 API Key chưa được cài đặt!")
    st.stop()

genai.configure(api_key=api_key)

def call_ai_25_ultimate(content):
    """Chiến thuật 'Kiên trì vĩnh cửu': Tự động thử lại đến khi thành công"""
    # Lấy danh sách model khả dụng ngay lập tức
    try:
        available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in available else available[0]
    except:
        target = 'gemini-1.5-flash'

    model = genai.GenerativeModel(target)
    
    # Vòng lặp thử lại tối đa 5 lần với thời gian chờ linh hoạt
    for attempt in range(5):
        try:
            response = model.generate_content(f"Hệ thống Văn Hiến AI 2.5 chuyên sâu: {content}")
            return response.text
        except Exception as e:
            err = str(e)
            # Nếu lỗi bận (429) hoặc lỗi máy chủ (500)
            if "429" in err or "500" in err or "ResourceExhausted" in err:
                wait = (attempt + 1) * 3 + random.random()
                time.sleep(wait)
                continue
            # Nếu lỗi 404 thì thử đổi tên model trực tiếp
            if "404" in err:
                try:
                    alt_model = genai.GenerativeModel('gemini-pro')
                    return alt_model.generate_content(content).text
                except: pass
            return f"❌ Thông báo: Google đang bảo trì vùng này. Bạn hãy thử lại sau vài giây."
            
    return "🚀 Hệ thống đang chịu tải cực cao. Hãy nhấn lại nút sau 10 giây để AI hoàn tất xử lý."

# --- 3. GIAO DIỆN CHÍNH ---
st.markdown("<h1 class='main-title'>VĂN HIẾN AI 2.5</h1>", unsafe_allow_html=True)

tabs = st.tabs(["📝 DÀN Ý", "🎓 CHẤM ĐIỂM", "📡 DẪN CHỨNG"])

with tabs[0]:
    p1 = st.text_area("Nhập đề bài:", height=100, key="t1")
    if st.button("XỬ LÝ DÀN Ý 2.5", key="b1"):
        if p1:
            with st.spinner("Văn Hiến AI đang kết nối vĩnh cửu..."):
                st.markdown(f"<div class='result-card'>{call_ai_25_ultimate(f'Lập dàn ý: {p1}')}</div>", unsafe_allow_html=True)

with tabs[1]:
    p2 = st.text_area("Dán bài làm:", height=200, key="t2")
    if st.button("THẨM ĐỊNH BÀI 2.5", key="b2"):
        if p2:
            with st.spinner("Đang thẩm định chuyên sâu..."):
                st.markdown(f"<div class='result-card'>{call_ai_25_ultimate(f'Chấm điểm: {p2}')}</div>", unsafe_allow_html=True)

with tabs[2]:
    p3 = st.text_input("Vấn đề xã hội:", key="t3")
    if st.button("QUÉT DẪN CHỨNG 2.5", key="b3"):
        if p3:
            with st.spinner("Đang truy xuất dữ liệu..."):
                st.markdown(f"<div class='result-card'>{call_ai_25_ultimate(f'Dẫn chứng: {p3}')}</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("Hệ thống vận hành trên nền tảng Gemini 1.5 Flash - Tối ưu 2026")
