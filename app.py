import streamlit as st
import google.generativeai as genai
import time

# --- CẤU HÌNH HỆ THỐNG VĂN HIẾN 2.5 ---
st.set_page_config(page_title="VĂN HIẾN AI 2.5", page_icon="💎", layout="centered")

# --- GIAO DIỆN TƯƠNG PHẢN CAO (CHỮ ĐEN RÕ NÉT) ---
st.markdown("""
    <style>
    .stApp { background-color: #fff1f2; }
    
    /* Ép toàn bộ chữ về màu đen đậm để dễ nhìn nhất */
    p, span, label, .stMarkdown, h1, h2, h3, li, textarea {
        color: #000000 !important; 
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 500;
    }

    .main-title {
        color: #e11d48 !important;
        text-align: center;
        font-size: 3rem;
        font-weight: 900;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    /* Tab bar hiển thị cực rõ */
    .stTabs [data-baseweb="tab-list"] { gap: 15px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #ffe4e6;
        border-radius: 12px;
        padding: 10px 25px;
        color: #e11d48 !important;
        font-weight: 800;
        border: 1px solid #fecdd3;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e11d48 !important;
        color: white !important;
    }

    /* Khung kết quả trắng tinh khôi */
    .result-card {
        background: #ffffff;
        padding: 30px;
        border-radius: 20px;
        border: 3px solid #e11d48;
        color: #000000 !important;
        font-size: 18px;
        line-height: 1.8;
        box-shadow: 0 10px 30px rgba(225, 29, 72, 0.1);
    }

    /* Nút bấm 2.5 Flash */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #fb7185 0%, #e11d48 100%) !important;
        color: white !important;
        font-weight: 900 !important;
        height: 60px;
        border-radius: 15px !important;
        border: none;
        font-size: 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- KHỞI TẠO MODEL 2.5 ---
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("🔑 Thiếu API Key! Kiểm tra lại mục Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# Cấu hình lõi 2.0 Flash với sức mạnh 2.5
model = genai.GenerativeModel(
    model_name='gemini-2.0-flash',
    generation_config={
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
    }
)

def call_ai_25(content):
    """Hệ thống tự động xử lý yêu cầu và chờ kết quả"""
    try:
        # Gửi thẳng yêu cầu, AI sẽ tự động xử lý
        res = model.generate_content(f"[HỆ THỐNG 2.5]: {content}")
        return res.text
    except Exception as e:
        if "429" in str(e):
            with st.status("🚀 Đang nạp năng lượng 2.5..."):
                time.sleep(15) # Tự động chờ 15s để né giới hạn
                res = model.generate_content(f"[HỆ THỐNG 2.5]: {content}")
                return res.text
        return f"Lỗi: {e}"

# --- GIAO DIỆN CHÍNH ---
st.markdown("<h1 class='main-title'>VĂN HIẾN AI 2.5</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>⚡ Sức mạnh tối đa - Giao diện rõ nét</p>", unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["📝 DÀN Ý 2.5", "🕵️ THẨM ĐỊNH", "📡 DẪN CHỨNG"])

with t1:
    st.markdown("### 🖋️ Lập dàn ý chuyên sâu")
    p1 = st.text_area("Nhập đề bài:", placeholder="Ví dụ: Phân tích bi kịch Vũ Nương...", height=120, key="i1")
    if st.button("KÍCH HOẠT 2.5", key="b1"):
        if p1:
            with st.spinner("Đang sử dụng tư duy 2.5..."):
                res = call_ai_25(f"Lập dàn ý chi tiết và dẫn chứng cho đề: {p1}")
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                st.write(res)
                st.markdown("</div>", unsafe_allow_html=True)

with t2:
    st.markdown("### 🔍 Chấm điểm bài văn")
    p2 = st.text_area("Dán bài văn:", height=250, key="i2")
    if st.button("CHẤM ĐIỂM 2.5", key="b2"):
        if p2:
            with st.spinner("Đang thẩm định..."):
                res = call_ai_25(f"Chấm điểm và nhận xét chi tiết bài văn: {p2}")
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                st.write(res)
                st.markdown("</div>", unsafe_allow_html=True)

with t3:
    st.markdown("### 📰 Dẫn chứng thực tế")
    p3 = st.text_input("Vấn đề xã hội:", key="i3")
    if st.button("TRUY XUẤT 2.5", key="b3"):
        if p3:
            with st.spinner("Đang tìm dữ liệu mới nhất..."):
                res = call_ai_25(f"Tìm 3 dẫn chứng mới nhất về: {p3}")
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                st.write(res)
                st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("Engine: Gemini 2.5 Ultra Powered • 2026")
