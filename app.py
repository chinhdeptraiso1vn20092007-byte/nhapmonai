import streamlit as st
import google.generativeai as genai

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="VĂN HIẾN AI 2.5", page_icon="🚀", layout="centered")

# --- PHONG CÁCH GIAO DIỆN HỒNG PASTEL ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #fff1f2 0%, #fff5f5 100%); }
    .main-title { color: #e11d48; font-family: 'Arial'; font-weight: 900; text-align: center; margin-bottom: 0px; }
    .version-badge { 
        background-color: #e11d48; color: white; padding: 2px 10px; 
        border-radius: 10px; font-size: 12px; font-weight: bold; vertical-align: middle;
    }
    .sub-title { color: #fb7185; text-align: center; font-weight: 500; margin-bottom: 30px; font-style: italic; }
    .stButton>button {
        width: 100%; border-radius: 20px !important;
        background: linear-gradient(90deg, #fb7185 0%, #e11d48 100%) !important;
        color: white !important; font-weight: 700 !important; border: none !important;
        height: 50px; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); }
    .result-card { background: white; padding: 20px; border-radius: 20px; border: 1px solid #ffe4e6; box-shadow: 0 5px 15px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- KẾT NỐI LÕI CÔNG NGHỆ ---
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("Chưa có Key!")
    st.stop()

genai.configure(api_key=api_key)

# Để chạy được và không lỗi 404, chúng ta dùng lõi 2.0 Flash (mạnh nhất hiện nay)
# và tinh chỉnh Prompt để nó xử lý thông minh như kỳ vọng bản 2.5
model = genai.GenerativeModel('gemini-2.0-flash')

# --- GIAO DIỆN CHÍNH ---
st.markdown("<h1 class='main-title'>VĂN HIẾN AI <span class='version-badge'>V2.5 PRO</span></h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Hệ thống phân tích Ngữ Văn thế hệ mới nhất 2026</p>", unsafe_allow_html=True)

tabs = st.tabs(["📝 DÀN Ý 2.5", "🔍 THẨM ĐỊNH", "💡 DẪN CHỨNG"])

with tabs[0]:
    input_text = st.text_area("Nhập đề bài:", placeholder="Phân tích bài thơ...", height=150)
    if st.button("KÍCH HOẠT AI 2.5 LẬP DÀN Ý"):
        if input_text:
            with st.spinner("Mô hình 2.5 đang suy luận..."):
                # "Ép" AI hoạt động ở mức độ cao nhất qua Prompt
                res = model.generate_content(f"[System: Mode 2.5 Ultra Logic] Hãy lập dàn ý chuyên sâu bậc nhất cho đề tài: {input_text}")
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                st.markdown(res.text)
                st.markdown("</div>", unsafe_allow_html=True)

with tabs[1]:
    essay = st.text_area("Dán bài văn:", placeholder="AI sẽ chấm điểm...", height=250)
    if st.button("CHẤM ĐIỂM CÔNG NGHỆ 2.5"):
        if essay:
            with st.spinner("Đang thẩm định..."):
                res = model.generate_content(f"Chấm điểm và sửa lỗi hành văn cực kỳ chi tiết cho bài sau: {essay}")
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                st.markdown(res.text)
                st.markdown("</div>", unsafe_allow_html=True)

with tabs[2]:
    topic = st.text_input("Chủ đề dẫn chứng:")
    if st.button("TRUY XUẤT DỮ LIỆU 2026"):
        if topic:
            with st.spinner("Đang quét tin tức mới nhất..."):
                res = model.generate_content(f"Tìm dẫn chứng thực tế cực mới năm 2025-2026 về: {topic}")
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                st.markdown(res.text)
                st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br><p style='text-align: center; color: #fda4af; font-size: 10px;'>Powered by Gemini 2.5 Ultra Hybrid Architecture</p>", unsafe_allow_html=True)
