import streamlit as st
import google.generativeai as genai
import time

# --- CẤU HÌNH ---
st.set_page_config(page_title="VĂN HIẾN AI 2.5", page_icon="📖", layout="centered")

# --- CSS TỐI ƯU HIỂN THỊ (TƯƠNG PHẢN CAO) ---
st.markdown("""
    <style>
    .stApp { background-color: #fff5f5; }
    p, span, label, .stMarkdown, h1, h2, h3 {
        color: #1a1a1a !important; 
        font-family: 'Arial', sans-serif;
    }
    .main-title {
        color: #e11d48 !important;
        text-align: center;
        font-size: 2.8rem;
        font-weight: 900;
        margin-bottom: 0px;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #ffe4e6;
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        color: #e11d48 !important;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e11d48 !important;
        color: white !important;
    }
    .result-card {
        background: #ffffff;
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #fb7185;
        color: #000000 !important;
        line-height: 1.7;
        margin-top: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .stButton>button {
        width: 100%;
        background: #e11d48 !important;
        color: white !important;
        font-weight: 800 !important;
        border-radius: 12px !important;
        height: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- KẾT NỐI AI ---
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("🔑 Chưa có API Key trong Secrets!")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

def call_ai_with_retry(content, max_retries=3):
    """Hàm tự động thử lại nếu hệ thống bận"""
    retries = 0
    delay = 5  # Giây chờ ban đầu
    
    while retries < max_retries:
        try:
            # Gửi yêu cầu tới Gemini
            res = model.generate_content(f"[Tư duy 2.5 chuyên sâu] {content}")
            return res.text
        except Exception as e:
            err_msg = str(e)
            # Nếu gặp lỗi quá tải (429) hoặc ResourceExhausted
            if "429" in err_msg or "ResourceExhausted" in err_msg:
                retries += 1
                if retries < max_retries:
                    st.warning(f"⚠️ Hệ thống đang bận (Lượt {retries}/{max_retries}). Đang tự động chờ {delay} giây để thử lại...")
                    time.sleep(delay)
                    delay *= 2  # Tăng thời gian chờ cho lần sau
                else:
                    return "❌ Rất tiếc, máy chủ Google đang quá tải. Bạn hãy vui lòng quay lại sau 1 phút nhé!"
            else:
                return f"⚠️ Lỗi kỹ thuật: {err_msg}"
    return None

# --- GIAO DIỆN ---
st.markdown("<h1 class='main-title'>VĂN HIẾN AI 2.5 PRO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold; color: #fb7185 !important;'>Tự động xử lý hàng chờ - Hiệu năng tối đa</p>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📝 LẬP DÀN Ý", "🕵️ CHẤM ĐIỂM", "📡 DẪN CHỨNG"])

with tab1:
    st.markdown("### 🖋️ Nhập đề bài văn học")
    de_bai = st.text_area("Đề bài:", placeholder="Ví dụ: Phân tích nhân vật Tràng...", height=100, key="txt1")
    if st.button("LẬP DÀN Ý NGAY", key="btn1"):
        if de_bai:
            with st.spinner("Đang kết nối với Gemini 2.5..."):
                result = call_ai_with_retry(f"Lập dàn ý chi tiết: {de_bai}")
                if result:
                    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                    st.write(result)
                    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("### 🔍 Thẩm định bài viết")
    bai_van = st.text_area("Dán bài văn:", placeholder="Dán nội dung tại đây...", height=200, key="txt2")
    if st.button("CHẤM ĐIỂM CHI TIẾT", key="btn2"):
        if bai_van:
            with st.spinner("Đang phân tích sâu..."):
                result = call_ai_with_retry(f"Chấm điểm và sửa bài văn: {bai_van}")
                if result:
                    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                    st.write(result)
                    st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    st.markdown("### 📰 Kho dẫn chứng 2.5")
    chu_de = st.text_input("Vấn đề xã hội:", placeholder="Ví dụ: Lòng biết ơn...", key="txt3")
    if st.button("TÌM DẪN CHỨNG MỚI", key="btn3"):
        if chu_de:
            with st.spinner("Đang tra cứu dữ liệu..."):
                result = call_ai_with_retry(f"Tìm dẫn chứng mới nhất về: {chu_de}")
                if result:
                    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                    st.write(result)
                    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 12px;'>Phiên bản Core 2.5 PRO • 2026</p>", unsafe_allow_html=True)
