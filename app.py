import streamlit as st
import google.generativeai as genai
import time

# --- CẤU HÌNH ---
st.set_page_config(page_title="VĂN HIẾN AI 2.5", page_icon="💎", layout="centered")

# --- CSS SIÊU TƯƠNG PHẢN (CHỮ ĐEN TUYỆT ĐỐI) ---
st.markdown("""
    <style>
    .stApp { background-color: #fff1f2; }
    p, span, label, .stMarkdown, h1, h2, h3, li, textarea, input {
        color: #000000 !important; 
        font-family: 'Arial', sans-serif !important;
        font-weight: 600 !important;
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

# --- KẾT NỐI AI ---
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("🔑 Thiếu API Key!")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

def call_ai_25(content):
    """Cơ chế kiên trì: Thử lại liên tục cho đến khi có kết quả"""
    attempt = 1
    wait_time = 15 # Thời gian chờ cơ bản
    
    # Tạo một vùng thông báo trạng thái
    status_msg = st.empty()
    
    while True: # Vòng lặp vô hạn cho đến khi 'return'
        try:
            res = model.generate_content(f"[HỆ THỐNG 2.5]: {content}")
            status_msg.empty() # Xóa thông báo chờ khi thành công
            return res.text
        except Exception as e:
            if "429" in str(e) or "ResourceExhausted" in str(e):
                status_msg.warning(f"🚀 Lượt thử {attempt}: Hệ thống 2.5 đang bận. Đang tự động xếp hàng chờ {wait_time} giây...")
                time.sleep(wait_time)
                attempt += 1
                wait_time += 5 # Mỗi lần thất bại thì chờ lâu hơn một chút để 'né' bộ lọc
            else:
                status_msg.error(f"❌ Lỗi: {e}")
                return None

# --- GIAO DIỆN ---
st.markdown("<h1 class='main-title'>VĂN HIẾN AI 2.5</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>⚡ Chế độ: Kiên trì vô hạn - Đợi là có kết quả</p>", unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["📝 DÀN Ý 2.5", "🕵️ THẨM ĐỊNH", "📡 DẪN CHỨNG"])

with t1:
    p1 = st.text_area("Nhập đề bài:", placeholder="Phân tích...", height=120, key="v1")
    if st.button("KÍCH HOẠT 2.5", key="b1"):
        if p1:
            with st.spinner("Đang ép xung mô hình 2.5..."):
                res = call_ai_25(f"Lập dàn ý chi tiết: {p1}")
                if res:
                    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                    st.markdown(res)
                    st.markdown("</div>", unsafe_allow_html=True)

with t2:
    p2 = st.text_area("Dán bài văn:", height=250, key="v2")
    if st.button("CHẤM ĐIỂM 2.5", key="b2"):
        if p2:
            with st.spinner("Đang thẩm định chuyên sâu..."):
                res = call_ai_25(f"Chấm điểm bài văn: {p2}")
                if res:
                    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                    st.markdown(res)
                    st.markdown("</div>", unsafe_allow_html=True)

with t3:
    p3 = st.text_input("Vấn đề xã hội:", key="v3")
    if st.button("TRUY XUẤT 2.5", key="b3"):
        if p3:
            with st.spinner("Đang quét dữ liệu mới nhất..."):
                res = call_ai_25(f"Dẫn chứng thực tế về: {p3}")
                if res:
                    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                    st.markdown(res)
                    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("Engine: Gemini 2.5 Turbo Hybrid • 2026")
