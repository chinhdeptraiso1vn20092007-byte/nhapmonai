import streamlit as st
import google.generativeai as genai
import time

# --- CẤU HÌNH HỆ THỐNG ---
st.set_page_config(page_title="VĂN HIẾN AI 2.5", page_icon="💎", layout="centered")

# --- CSS SIÊU TƯƠNG PHẢN (CHỮ ĐEN ĐẬM 100%) ---
st.markdown("""
    <style>
    .stApp { background-color: #fff1f2; }
    p, span, label, .stMarkdown, h1, h2, h3, li, textarea, input {
        color: #000000 !important; 
        font-family: 'Arial', sans-serif !important;
        font-weight: 800 !important; /* Siêu đậm để nhìn rõ */
    }
    .main-title { color: #e11d48 !important; text-align: center; font-size: 2.8rem; font-weight: 900; }
    .stTabs [data-baseweb="tab"] {
        background-color: #ffe4e6; border-radius: 10px; padding: 10px 20px;
        color: #e11d48 !important; font-weight: 800;
    }
    .stTabs [aria-selected="true"] { background-color: #e11d48 !important; color: white !important; }
    .result-card {
        background: #ffffff; padding: 25px; border-radius: 20px;
        border: 3px solid #e11d48; color: #000000 !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    .stButton>button {
        width: 100%; background: #e11d48 !important; color: white !important;
        font-weight: 900 !important; height: 60px; border-radius: 15px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- KẾT NỐI & TỰ ĐỘNG DÒ MODEL ---
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("🔑 Thiếu API Key!")
    st.stop()

genai.configure(api_key=api_key)

def get_best_model():
    """Hàm tự động quét danh sách model khả dụng"""
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Ưu tiên các dòng Flash vì tốc độ và hạn mức cao
        priority_list = [
            'models/gemini-2.0-flash', 
            'models/gemini-1.5-flash-latest', 
            'models/gemini-1.5-flash',
            'models/gemini-pro'
        ]
        for p in priority_list:
            if p in models:
                return genai.GenerativeModel(p)
        return genai.GenerativeModel(models[0]) # Nếu không có trong ưu tiên, lấy cái đầu tiên tìm được
    except:
        return genai.GenerativeModel('gemini-1.5-flash') # Phương án dự phòng cuối cùng

# Khởi tạo model tự động
active_model = get_best_model()

def call_ai_smart(content):
    try:
        res = active_model.generate_content(f"Đóng vai chuyên gia văn học 2.5: {content}")
        return res.text
    except Exception as e:
        if "429" in str(e):
            st.warning("⏳ Đang xếp hàng chờ Google xử lý (10s)...")
            time.sleep(10)
            return "Hệ thống vừa bận, bạn vui lòng bấm lại một lần nữa nhé!"
        return f"❌ Lỗi: {e}"

# --- GIAO DIỆN ---
st.markdown("<h1 class='main-title'>VĂN HIẾN AI 2.5</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #fb7185 !important;'>🤖 Đang sử dụng lõi: {active_model.model_name}</p>", unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["📝 DÀN Ý", "🕵️ CHẤM ĐIỂM", "📡 DẪN CHỨNG"])

with t1:
    p1 = st.text_area("Nhập đề bài:", height=100, key="k1")
    if st.button("LẬP DÀN Ý 2.5", key="b1"):
        if p1:
            with st.spinner("Đang xử lý dữ liệu..."):
                res = call_ai_smart(f"Lập dàn ý chi tiết: {p1}")
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                st.markdown(res)
                st.markdown("</div>", unsafe_allow_html=True)

with t2:
    p2 = st.text_area("Dán bài văn:", height=200, key="k2")
    if st.button("CHẤM ĐIỂM 2.5", key="b2"):
        if p2:
            with st.spinner("Đang thẩm định..."):
                res = call_ai_smart(f"Chấm điểm bài văn: {p2}")
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                st.markdown(res)
                st.markdown("</div>", unsafe_allow_html=True)

with t3:
    p3 = st.text_input("Vấn đề xã hội:", key="k3")
    if st.button("TRUY XUẤT 2.5", key="b3"):
        if p3:
            with st.spinner("Đang quét dẫn chứng..."):
                res = call_ai_smart(f"Dẫn chứng về: {p3}")
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                st.markdown(res)
                st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("Chế độ: Tự động dò tìm Model (Auto-Scan) • 2026")
