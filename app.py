import streamlit as st
from google import genai
import hashlib
import html

st.set_page_config(page_title="VĂN HIẾN AI 2.5", page_icon="💎")

# --- LẤY DANH SÁCH KEY ---
api_keys = st.secrets.get("GEMINI_API_KEYS", [])

if not api_keys:
    st.error("❌ Chưa có API key!")
    st.stop()

# --- CACHE ---
if "cache" not in st.session_state:
    st.session_state.cache = {}

def get_cache_key(text):
    return hashlib.md5(text.encode()).hexdigest()

# --- FALLBACK OFFLINE ---
def offline_fallback(prompt):
    if "dũng cảm" in prompt.lower():
        return """Dẫn chứng về lòng dũng cảm:

- Nguyễn Ngọc Ký: vượt qua khuyết tật để trở thành nhà giáo.
- Các y bác sĩ tuyến đầu chống dịch COVID-19.
- Nhân vật Phùng trong "Chiếc thuyền ngoài xa" dám nhìn thẳng vào sự thật.

→ Lòng dũng cảm là sức mạnh giúp con người vượt qua nghịch cảnh."""
    return "⚠️ Hệ thống đang bận, vui lòng thử lại sau."

# --- GỌI AI VỚI ROTATION ---
def call_ai(prompt):
    cache_key = get_cache_key(prompt)

    # dùng cache trước
    if cache_key in st.session_state.cache:
        return st.session_state.cache[cache_key]

    for key in api_keys:
        try:
            client = genai.Client(api_key=key)

            res = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            if res and res.text:
                result = res.text.strip()
                st.session_state.cache[cache_key] = result
                return result

        except Exception as e:
            if "429" in str(e):
                continue
            return f"❌ Lỗi: {e}"

    # nếu tất cả key đều hết quota
    return offline_fallback(prompt)

# --- HIỂN THỊ ---
def show(text):
    safe = html.escape(text)
    st.markdown(f"<div style='border:2px solid red;padding:15px'>{safe}</div>", unsafe_allow_html=True)

# --- UI ---
st.title("💎 VĂN HIẾN AI 2.5")

tab1, tab2, tab3 = st.tabs(["📝 LẬP DÀN Ý", "🎓 CHẤM ĐIỂM", "📡 DẪN CHỨNG"])

with tab3:
    p = st.text_input("Nhập vấn đề:")

    if st.button("TÌM"):
        if p:
            with st.spinner("Đang xử lý..."):
                result = call_ai(f"Tìm dẫn chứng cho: {p}")
                show(result)
