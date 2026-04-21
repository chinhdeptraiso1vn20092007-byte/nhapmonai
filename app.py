import streamlit as st
import google.generativeai as genai
import time
import random
import html

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
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: #be123c !important;
        transform: scale(1.02);
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

api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("🔑 Thiếu GEMINI_API_KEY trong Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)

MODEL_NAME = "gemini-2.5-flash"

def call_ai_ultimate(content: str) -> str:
    try:
        model = genai.GenerativeModel(model_name=MODEL_NAME)
    except Exception as e:
        return f"❌ Không khởi tạo được model {MODEL_NAME}: {e}"

    max_attempts = 5

    for i in range(max_attempts):
        try:
            full_prompt = f"""
Bạn là chuyên gia Văn Hiến AI 2.5.
Hãy thực hiện yêu cầu sau một cách chuyên nghiệp, rõ ràng, mạch lạc, đúng chính tả:

{content}
"""
            response = model.generate_content(full_prompt)

            if hasattr(response, "text") and response.text:
                return response.text.strip()

            return "⚠️ AI không trả về nội dung văn bản."

        except Exception as e:
            err = str(e).lower()

            if any(x in err for x in ["429", "resource", "quota", "500", "503", "limit", "unavailable"]):
                wait_time = min((i + 1) * 2 + random.random(), 10)
                time.sleep(wait_time)
                continue

            return f"❌ Lỗi hệ thống: {e}"

    return "🚀 Máy chủ đang bận. Bạn thử lại sau ít giây nhé."

def render_result(text: str):
    safe_text = html.escape(text)
    st.markdown(f"<div class='result-card'>{safe_text}</div>", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>VĂN HIẾN AI 2.5</h1>", unsafe_allow_html=True)

tabs = st.tabs(["📝 LẬP DÀN Ý", "🎓 CHẤM ĐIỂM", "📡 DẪN CHỨNG"])

with tabs[0]:
    p1 = st.text_area("Nhập đề bài văn học:", height=120, key="area1")
    if st.button("LẬP DÀN Ý TỨC THÌ", key="btn1"):
        if p1.strip():
            with st.spinner("AI đang lập dàn ý..."):
                res = call_ai_ultimate(f"Lập dàn ý chi tiết cho đề bài văn học sau:\n{p1}")
                render_result(res)

with tabs[1]:
    p2 = st.text_area("Dán nội dung bài làm:", height=250, key="area2")
    if st.button("THẨM ĐỊNH BÀI VIẾT", key="btn2"):
        if p2.strip():
            with st.spinner("AI đang đọc và chấm bài..."):
                res = call_ai_ultimate(
                    f"""Chấm điểm và nhận xét chi tiết bài văn sau.
Yêu cầu:
- Nhận xét ưu điểm
- Chỉ ra hạn chế
- Góp ý sửa lỗi
- Cho điểm tham khảo

Bài làm:
{p2}"""
                )
                render_result(res)

with tabs[2]:
    p3 = st.text_input("Vấn đề cần tìm dẫn chứng:", key="input3")
    if st.button("TRUY XUẤT DỮ LIỆU", key="btn3"):
        if p3.strip():
            with st.spinner("AI đang tìm dẫn chứng..."):
                res = call_ai_ultimate(
                    f"Tìm các dẫn chứng thời sự, xã hội, đời sống phù hợp để viết văn nghị luận về chủ đề: {p3}"
                )
                render_result(res)

st.markdown("---")
st.caption("Hệ thống sử dụng Gemini 2.5 Flash • Văn Hiến AI 2.5")
