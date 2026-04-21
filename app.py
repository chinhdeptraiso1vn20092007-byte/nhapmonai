import streamlit as st
import google.generativeai as genai
import time

# --- CẤU HÌNH GIAO DIỆN SIÊU RÕ ---
st.set_page_config(page_title="VĂN HIẾN AI 2.5", page_icon="💎", layout="centered")

st.markdown("""
    <style>
    /* Nền trắng tinh để chữ đen nổi nhất */
    .stApp { background-color: #ffffff; }
    
    /* Ép tất cả chữ thành màu đen đậm tuyệt đối */
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
    }

    /* Tab bar rõ mồn một */
    .stTabs [data-baseweb="tab"] {
        background-color: #f1f5f9; border-radius: 10px; padding: 12px 25px;
        color: #000000 !important; font-weight: 800; border: 1px solid #cbd5e1;
    }
    .stTabs [aria-selected="true"] { 
        background-color: #e11d48 !important; color: white !important; 
    }

    /* Nút bấm đỏ rực */
    .stButton>button {
        width: 100%; background: #e11d48 !important; color: white !important;
        font-weight: 900 !important; height: 65px; border-radius: 15px !important;
        font-size: 1.3rem !important;
    }

    /* Khung kết quả rành mạch */
    .result-card {
        background: #ffffff; padding: 25px; border-radius: 15px;
        border: 4px solid #e11d48; color: #000000 !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        margin-top: 20px; font-size: 1.1rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CẤU HÌNH AI ---
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("🔑 Thiếu API Key trong phần Secrets!")
    st.stop()

genai.configure(api_key=api_key)

def call_ai_power(content):
    """Chiến thuật tối ưu: Thử model 1.5 Flash trước vì nó ít khi báo bận"""
    # Chỉ tập trung vào 1.5 Flash vì nó là model ổn định nhất cho gói Free
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(f"Chuyên gia Văn học 2.5 xử lý đề bài: {content}")
        return res.text
    except Exception as e:
        if "429" in str(e) or "ResourceExhausted" in str(e):
            # Nếu bận, tự động đợi 5s và thử lại đúng 1 lần duy nhất với model Pro
            time.sleep(5)
            try:
                model_pro = genai.GenerativeModel('gemini-1.5-pro')
                res = model_pro.generate_content(content)
                return res.text
            except:
                return "⚠️ Hiện tại Google đang thắt chặt băng thông miễn phí. Bạn vui lòng đợi 15 giây rồi nhấn lại nút nhé!"
        return f"❌ Lỗi: {e}"

# --- GIAO DIỆN CHÍNH ---
st.markdown("<h1 class='main-title'>VĂN HIẾN AI 2.5</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #e11d48 !important;'>Hệ thống Phân tích Văn học Siêu tốc</p>", unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["📝 DÀN Ý", "🕵️ CHẤM ĐIỂM", "📡 DẪN CHỨNG"])

with t1:
    p1 = st.text_area("Nhập đề bài văn học:", height=120, key="t1")
    if st.button("LẬP DÀN Ý TỨC THÌ", key="b1"):
        if p1:
            with st.spinner("Đang kết nối siêu tốc..."):
                res = call_ai_power(f"Lập dàn ý chi tiết: {p1}")
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                st.write(res)
                st.markdown("</div>", unsafe_allow_html=True)

with t2:
    p2 = st.text_area("Dán bài làm tại đây:", height=200, key="t2")
    if st.button("THẨM ĐỊNH NGAY", key="b2"):
        if p2:
            with st.spinner("Đang soi lỗi văn bản..."):
                res = call_ai_power(f"Chấm điểm bài văn: {p2}")
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                st.write(res)
                st.markdown("</div>", unsafe_allow_html=True)

with t3:
    p3 = st.text_input("Vấn đề xã hội:", key="t3")
    if st.button("TÌM DẪN CHỨNG", key="b3"):
        if p3:
            with st.spinner("Đang tra cứu dữ liệu..."):
                res = call_ai_power(f"Dẫn chứng về: {p3}")
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                st.write(res)
                st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("Bản cập nhật Siêu Tương Phản & Tối Ưu Quota • 2026")
