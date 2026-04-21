import streamlit as st
import google.generativeai as genai
import time

# --- CẤU HÌNH ---
st.set_page_config(page_title="VĂN HIẾN AI 2.5", page_icon="💎", layout="centered")

# --- CSS SIÊU ĐẬM - SIÊU RÕ ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    /* Làm chữ to và đen đậm tuyệt đối */
    p, span, label, .stMarkdown, h1, h2, h3, li, textarea, input {
        color: #000000 !important; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
    }
    .main-title { color: #e11d48 !important; text-align: center; font-size: 3.5rem !important; font-weight: 900 !important; }
    
    /* Làm nổi bật các Tab */
    .stTabs [data-baseweb="tab"] {
        background-color: #f1f5f9; border-radius: 12px; padding: 15px 30px;
        color: #475569 !important; border: 2px solid #e2e8f0;
    }
    .stTabs [aria-selected="true"] { background-color: #e11d48 !important; color: white !important; border: 2px solid #e11d48; }
    
    /* Nút bấm siêu to */
    .stButton>button {
        width: 100%; background: #e11d48 !important; color: white !important;
        font-weight: 900 !important; height: 70px; border-radius: 20px !important; font-size: 20px !important;
    }
    .result-card {
        background: #f8fafc; padding: 30px; border-radius: 25px;
        border: 4px solid #e11d48; color: #000000 !important; font-size: 19px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- KẾT NỐI AI ---
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("🔑 Bạn chưa nhập API Key vào phần Secrets của Streamlit!")
    st.stop()

genai.configure(api_key=api_key)

def call_ai_final_boss(content):
    """Cơ chế tự động dò tìm và kiên trì đến cùng"""
    # Danh sách model từ cao xuống thấp
    models_to_try = ['gemini-1.5-flash-latest', 'gemini-1.5-flash', 'gemini-pro']
    
    status = st.empty()
    
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            # Thử gửi yêu cầu
            res = model.generate_content(f"Chuyên gia Ngữ văn 2.5 hãy giải quyết: {content}", 
                                         generation_config={"temperature": 0.7})
            status.empty()
            return res.text
        except Exception as e:
            if "429" in str(e) or "ResourceExhausted" in str(e):
                status.warning(f"🚀 Model {model_name} đang nghẽn. Đang tự động chuyển model khác và chờ 10s...")
                time.sleep(10)
                continue # Thử model tiếp theo
            else:
                continue
                
    return "❌ Hiện tại tất cả các model đều bận do giới hạn của Google. Bạn vui lòng đợi 1-2 phút rồi nhấn 'Thử lại' nhé!"

# --- GIAO DIỆN ---
st.markdown("<h1 class='main-title'>VĂN HIẾN AI 2.5</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Bản Cứu Trợ Khẩn Cấp - Tự Động Vượt Lỗi Quá Tải</p>", unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["📝 DÀN Ý 2.5", "🕵️ THẨM ĐỊNH", "📡 DẪN CHỨNG"])

with t1:
    p1 = st.text_area("Nhập đề bài:", height=100, key="k1")
    if st.button("LẬP DÀN Ý NGAY", key="b1"):
        if p1:
            with st.spinner("Hệ thống 2.5 đang tìm đường kết nối..."):
                res = call_ai_final_boss(f"Lập dàn ý chi tiết bài: {p1}")
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                st.write(res)
                st.markdown("</div>", unsafe_allow_html=True)

with t2:
    p2 = st.text_area("Dán bài văn:", height=200, key="k2")
    if st.button("CHẤM ĐIỂM NGAY", key="b2"):
        if p2:
            with st.spinner("Đang thẩm định bài viết..."):
                res = call_ai_final_boss(f"Chấm điểm và nhận xét: {p2}")
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                st.write(res)
                st.markdown("</div>", unsafe_allow_html=True)

with t3:
    p3 = st.text_input("Vấn đề xã hội:", key="k3")
    if st.button("TRUY XUẤT DẪN CHỨNG", key="b3"):
        if p3:
            with st.spinner("Đang tra cứu dữ liệu thực tế..."):
                res = call_ai_with_retry(f"Dẫn chứng thực tế về: {p3}")
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                st.write(res)
                st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("Version: 2.5 Rescue Edition • 2026")
