import streamlit as st
from google import genai
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
    st.error("🔑 Thiếu GEMINI_API_KEY trong Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

PRIMARY_MODEL = "gemini-2.5-flash"
FALLBACK_MODEL = "gemini-2.0-flash"

def call_model(model_name: str, prompt: str) -> str:
    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )
    if getattr(response, "text", None):
        return response.text.strip()
    raise RuntimeError(f"Model {model_name} không trả về nội dung.")

def friendly_quota_message():
    return (
        "🚫 Hệ thống AI hiện tạm hết lượt sử dụng.\n\n"
        "Bạn vui lòng thử lại sau ít phút hoặc đổi API key khác.\n\n"
        "Cách xử lý:\n"
        "- Chờ quota reset\n"
        "- Tạo API key / project mới trong Google AI Studio\n"
        "- Nâng gói nếu cần dùng thường xuyên"
    )

def call_ai(content: str) -> str:
    prompt = f"""
Bạn là giáo viên Ngữ Văn giỏi.
Hãy trả lời rõ ràng, có bố cục, đúng chính tả.

{content}
"""

    try:
        return call_model(PRIMARY_MODEL, prompt)
    except Exception as e1:
        err1 = str(e1).lower()

        if "429" in err1 or "resource_exhausted" in err1 or "quota" in err1:
            try:
                return call_model(FALLBACK_MODEL, prompt)
            except Exception as e2:
                err2 = str(e2).lower()
                if "429" in err2 or "resource_exhausted" in err2 or "quota" in err2:
                    return friendly_quota_message()
                return f"❌ Lỗi model dự phòng: {e2}"

        return f"❌ Lỗi hệ thống: {e1}"

def show_result(text: str):
    safe_text = html.escape(text)
    st.markdown(f"<div class='result-card'>{safe_text}</div>", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>VĂN HIẾN AI 2.5</h1>", unsafe_allow_html=True)

tabs = st.tabs(["📝 LẬP DÀN Ý", "🎓 CHẤM ĐIỂM", "📡 DẪN CHỨNG"])

with tabs[0]:
    p1 = st.text_area("Nhập đề bài văn học:", height=120)
    if st.button("LẬP DÀN Ý"):
        if p1.strip():
            with st.spinner("AI đang xử lý..."):
                show_result(call_ai(f"Lập dàn ý chi tiết cho đề bài:\n{p1}"))
        else:
            st.warning("Bạn chưa nhập đề.")

with tabs[1]:
    p2 = st.text_area("Dán bài văn:", height=250)
    if st.button("CHẤM BÀI"):
        if p2.strip():
            with st.spinner("AI đang chấm..."):
                show_result(call_ai(f"""
Chấm bài văn:
- Nhận xét
- Sửa lỗi
- Góp ý
- Cho điểm

Bài:
{p2}
"""))
        else:
            st.warning("Bạn chưa nhập bài.")

with tabs[2]:
    p3 = st.text_input("Nhập vấn đề:")
    if st.button("TÌM DẪN CHỨNG"):
        if p3.strip():
            with st.spinner("AI đang tìm..."):
                show_result(call_ai(f"Tìm dẫn chứng thực tế cho: {p3}"))
        else:
            st.warning("Bạn chưa nhập.")

st.markdown("---")
st.caption("Ưu tiên Gemini 2.5 Flash • dự phòng Gemini 2.0 Flash")
