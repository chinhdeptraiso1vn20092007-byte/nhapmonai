import streamlit as st
from google import genai
import time
import random
import html

# --- 1. GIAO DIỆN ---
st.set_page_config(page_title="VĂN HIẾN AI 2.5", page_icon="💎", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    p, span, label, .stMarkdown, h1, h2, h3, li, textarea, input {
        color: #000000 !important;
        font-family: Arial, sans-serif !important;
        font-weight: 800 !important;
    }
    .main-title {
        color: #e11d48 !important;
        text-align: center;
        font-size: 3.2rem !important;
        font-weight: 900 !important;
    }
    .stButton>button {
        width: 100%;
        background: #e11d48 !important;
        color: white !important;
        font-weight: 900 !important;
        height: 60px;
        border-radius: 15px !important;
        font-size: 1.15rem !important;
        border: none !important;
    }
    .result-card {
        background: #ffffff;
        padding: 22px;
        border-radius: 15px;
        border: 3px solid #e11d48;
        color: #000000 !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        margin-top: 18px;
        line-height: 1.7;
        white-space: pre-wrap;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. API KEY ---
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("🔑 Thiếu GEMINI_API_KEY trong Secrets!")
    st.stop()

# --- 3. KHỞI TẠO AI ---
client = genai.Client(api_key=api_key)
MODEL_NAME = "gemini-2.5-flash"

# --- 4. HÀM GỌI AI ---
def call_ai(content: str) -> str:
    max_attempts = 3

    for i in range(max_attempts):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=f"""
Bạn là giáo viên Ngữ Văn giỏi.
Trả lời rõ ràng, có bố cục:

{content}
"""
            )

            # Lấy nội dung an toàn
            if response and response.text:
                return response.text.strip()

            return "⚠️ AI không trả nội dung."

        except Exception as e:
            err = str(e).lower()

            # Retry khi server bận
            if any(x in err for x in ["429", "quota", "503", "unavailable"]):
                time.sleep((i + 1) * 2)
                continue

            # Hiện lỗi thật
            return f"❌ Lỗi hệ thống: {e}"

    return "🚀 Server đang bận, thử lại sau vài giây."

# --- 5. HIỂN THỊ KẾT QUẢ ---
def show_result(text):
    safe_text = html.escape(text)
    st.markdown(f"<div class='result-card'>{safe_text}</div>", unsafe_allow_html=True)

# --- 6. GIAO DIỆN CHÍNH ---
st.markdown("<h1 class='main-title'>VĂN HIẾN AI 2.5</h1>", unsafe_allow_html=True)

tabs = st.tabs(["📝 LẬP DÀN Ý", "🎓 CHẤM ĐIỂM", "📡 DẪN CHỨNG"])

# --- TAB 1 ---
with tabs[0]:
    p1 = st.text_area("Nhập đề bài văn học:", height=120)

    if st.button("LẬP DÀN Ý"):
        if p1.strip():
            with st.spinner("AI đang xử lý..."):
                res = call_ai(f"Lập dàn ý chi tiết cho đề bài:\n{p1}")
                show_result(res)
        else:
            st.warning("Bạn chưa nhập đề.")

# --- TAB 2 ---
with tabs[1]:
    p2 = st.text_area("Dán bài văn:", height=250)

    if st.button("CHẤM BÀI"):
        if p2.strip():
            with st.spinner("AI đang chấm..."):
                res = call_ai(f"""
Chấm bài văn:
- Nhận xét
- Sửa lỗi
- Góp ý
- Cho điểm

Bài:
{p2}
""")
                show_result(res)
        else:
            st.warning("Bạn chưa nhập bài.")

# --- TAB 3 ---
with tabs[2]:
    p3 = st.text_input("Nhập vấn đề:")

    if st.button("TÌM DẪN CHỨNG"):
        if p3.strip():
            with st.spinner("AI đang tìm..."):
                res = call_ai(f"Tìm dẫn chứng thực tế cho: {p3}")
                show_result(res)
        else:
            st.warning("Bạn chưa nhập.")

st.markdown("---")
st.caption("Gemini 2.5 Flash • Văn Hiến AI 2026")
