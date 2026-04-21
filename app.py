import streamlit as st
import google.generativeai as genai

# --- CẤU HÌNH ---
st.set_page_config(page_title="VĂN HIẾN AI 2.5", page_icon="💎", layout="centered")

# --- CSS SIÊU TƯƠNG PHẢN (CHỮ ĐEN ĐẬM, DỄ NHÌN) ---
st.markdown("""
    <style>
    .stApp { background-color: #fff1f2; }
    p, span, label, .stMarkdown, h1, h2, h3, li, textarea, input {
        color: #000000 !important; 
        font-family: 'Arial', sans-serif !important;
        font-weight: 700 !important;
    }
    .main-title { color: #e11d48 !important; text-align: center; font-size: 3rem; font-weight: 900; }
    .stTabs [data-baseweb="tab"] {
        background-color: #ffe4e6; border-radius: 10px; padding: 10px 20px;
        color: #e11d48 !important; font-weight: bold;
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

# --- KẾT NỐI AI SIÊU TỐC ---
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("🔑 Thiếu API Key!")
    st.stop()

genai.configure(api_key=api_key)

# Chuyển về 1.5 Flash để lấy kết quả NGAY LẬP TỨC (hạn mức cao nhất)
model = genai.GenerativeModel('gemini-1.5-flash')

def call_ai_fast(content):
    try:
        # Gửi thẳng yêu cầu, không qua vòng lặp chờ để ưu tiên tốc độ
        res = model.generate_content(f"Hãy đóng vai chuyên gia văn học 2.5, trả lời cực sâu sắc đề bài: {content}")
        return res.text
    except Exception as e:
        if "429" in str(e):
            return "⚠️ Google đang giới hạn tốc độ. Bạn hãy thử nhấn lại sau 5 giây nhé!"
        return f"❌ Lỗi: {e}"

# --- GIAO DIỆN ---
st.markdown("<h1 class='main-title'>VĂN HIẾN AI 2.5</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>⚡ Chế độ SIÊU TỐC - Trả kết quả tức thì</p>", unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["📝 DÀN Ý 2.5", "🕵️ THẨM ĐỊNH", "📡 DẪN CHỨNG"])

with t1:
    p1 = st.text_area("Nhập đề bài:", placeholder="Phân tích...", height=120, key="v1")
    if st.button("KÍCH HOẠT 2.5", key="b1"):
        if p1:
            with st.spinner("Đang truy xuất kết quả..."):
                res = call_ai_fast(f"Lập dàn ý chi tiết: {p1}")
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                st.markdown(res)
                st.markdown("</div>", unsafe_allow_html=True)

with t2:
    p2 = st.text_area("Dán bài văn:", height=250, key="v2")
    if st.button("CHẤM ĐIỂM 2.5", key="b2"):
        if p2:
            with st.spinner("Đang chấm điểm nhanh..."):
                res = call_ai_fast(f"Chấm điểm bài văn: {p2}")
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                st.markdown(res)
                st.markdown("</div>", unsafe_allow_html=True)

with t3:
    p3 = st.text_input("Vấn đề xã hội:", key="v3")
    if st.button("TRUY XUẤT 2.5", key="b3"):
        if p3:
            with st.spinner("Đang quét dữ liệu..."):
                res = call_ai_fast(f"Dẫn chứng thực tế về: {p3}")
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                st.markdown(res)
                st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("Powered by Gemini 1.5 Flash Turbo Core • 2026")
