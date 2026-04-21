import streamlit as st
import google.generativeai as genai
import time

# --- CẤU HÌNH HỆ THỐNG ---
st.set_page_config(page_title="VĂN HIẾN AI 2.5", page_icon="💎", layout="centered")

# --- CSS TỐI ƯU TƯƠNG PHẢN TUYỆT ĐỐI ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    
    /* Chữ đen đặc, to, dày để nhìn rõ 100% */
    p, span, label, .stMarkdown, h1, h2, h3, li, textarea, input {
        color: #000000 !important; 
        font-family: 'Arial', sans-serif !important;
        font-weight: 800 !important;
    }
    
    .main-title { 
        color: #e11d48 !important; 
        text-align: center; 
        font-size: 3rem !important; 
        font-weight: 900 !important;
        margin-bottom: 0px;
    }

    /* Tab rõ ràng */
    .stTabs [data-baseweb="tab"] {
        background-color: #f8fafc; border-radius: 10px; padding: 10px 20px;
        color: #e11d48 !important; border: 1px solid #e2e8f0;
    }
    .stTabs [aria-selected="true"] { 
        background-color: #e11d48 !important; color: white !important; 
    }

    /* Nút bấm nổi bật */
    .stButton>button {
        width: 100%; background: #e11d48 !important; color: white !important;
        font-weight: 900 !important; height: 60px; border-radius: 15px !important;
        font-size: 1.2rem !important;
    }

    /* Khung kết quả hiển thị cực rõ */
    .result-card {
        background: #ffffff; padding: 25px; border-radius: 15px;
        border: 4px solid #e11d48; color: #000000 !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- KHỞI TẠO AI ---
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("🔑 Lỗi: Chưa cấu hình API Key trong Secrets!")
    st.stop()

genai.configure(api_key=api_key)

def call_ai_final_boss(content):
    """Chiến thuật nhảy Model liên tục để thoát lỗi 429"""
    # Danh sách ưu tiên các model ổn định nhất
    models_to_try = [
        'gemini-1.5-flash-latest', 
        'gemini-1.5-flash', 
        'gemini-1.5-pro-latest',
        'gemini-pro'
    ]
    
    placeholder = st.empty()
    
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            res = model.generate_content(f"Chuyên gia Ngữ văn 2.5: {content}")
            placeholder.empty()
            return res.text
        except Exception as e:
            if "429" in str(e) or "ResourceExhausted" in str(e):
                placeholder.info(f"🔄 Cổng {model_name} đang bận, đang chuyển cổng dự phòng...")
                time.sleep(3) # Đợi ngắn để thử cổng khác
                continue
            else:
                continue
                
    return "⚠️ Google đang bảo trì toàn bộ cổng miễn phí. Bạn hãy đợi khoảng 30 giây rồi nhấn lại nút nhé!"

# --- GIAO DIỆN CHÍNH ---
st.markdown("<h1 class='main-title'>VĂN HIẾN AI 2.5</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Bản Fix Lỗi Toàn Diện - Trả Kết Quả Thông Suốt</p>", unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["📝 DÀN Ý", "🕵️ THẨM ĐỊNH", "📡 DẪN CHỨNG"])

with t1:
    st.markdown("### 🖋️ Nhập đề bài")
    p1 = st.text_area("Đề bài văn học:", height=100, key="input_t1")
    if st.button("LẬP DÀN Ý 2.5", key="btn_t1"):
        if p1:
            with st.spinner("Hệ thống 2.5 đang phân tích..."):
                res = call_ai_final_boss(f"Lập dàn ý chi tiết bài văn: {p1}")
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                st.write(res)
                st.markdown("</div>", unsafe_allow_html=True)

with t2:
    st.markdown("### 🔍 Chấm điểm bài văn")
    p2 = st.text_area("Dán bài làm tại đây:", height=200, key="input_t2")
    if st.button("CHẤM ĐIỂM NGAY", key="btn_t2"):
        if p2:
            with st.spinner("Đang thẩm định chất lượng..."):
                res = call_ai_final_boss(f"Chấm điểm và sửa bài văn: {p2}")
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                st.write(res)
                st.markdown("</div>", unsafe_allow_html=True)

with t3:
    st.markdown("### 📰 Dẫn chứng thực tế")
    p3 = st.text_input("Vấn đề xã hội:", key="input_t3")
    if st.button("TRUY XUẤT DẪN CHỨNG", key="btn_t3"):
        if p3:
            with st.spinner("Đang tìm kiếm dữ liệu mới..."):
                res = call_ai_final_boss(f"Tìm dẫn chứng thực tế cho: {p3}")
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                st.write(res)
                st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("Core: Gemini Hybrid Engine (Auto-Retry) • 2026")
