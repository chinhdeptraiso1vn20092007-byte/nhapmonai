import streamlit as st
import google.generativeai as genai
import time

# --- CẤU HÌNH HỆ THỐNG VĂN HIẾN AI 2.5 PRO ---
st.set_page_config(
    page_title="VĂN HIẾN AI 2.5", 
    page_icon="📖", 
    layout="centered"
)

# --- GIAO DIỆN TỐI ƯU HIỂN THỊ (CSS) ---
st.markdown("""
    <style>
    /* Nền ứng dụng */
    .stApp { 
        background-color: #fff1f2; 
    }
    
    /* Tiêu đề chính */
    .main-title { 
        color: #e11d48 !important; 
        font-family: 'Arial', sans-serif; 
        font-weight: 900; 
        text-align: center; 
        font-size: 2.5rem;
        margin-bottom: 5px;
    }
    
    .badge-25 {
        background-color: #e11d48; 
        color: white !important; 
        padding: 2px 12px; 
        border-radius: 10px;
        font-size: 14px;
    }

    /* Chữ trong toàn bộ ứng dụng phải là màu tối để dễ đọc */
    p, span, label, .stMarkdown {
        color: #334155 !important;
        font-weight: 500;
    }

    /* Khung kết quả trả về */
    .result-card {
        background: white; 
        padding: 20px; 
        border-radius: 15px;
        border: 2px solid #fecdd3; 
        color: #1e293b !important; /* Chữ đen đậm */
        line-height: 1.6;
        margin-top: 15px;
    }

    /* Tùy chỉnh Tab - Khắc phục lỗi không thấy chữ trên Tab */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #fce7f3;
        border-radius: 10px 10px 0 0;
        padding: 10px 15px;
        color: #e11d48 !important; /* Chữ trên tab màu đỏ */
    }
    .stTabs [aria-selected="true"] {
        background-color: #e11d48 !important;
        color: white !important;
    }

    /* Nút bấm */
    .stButton>button {
        width: 100%; 
        border-radius: 12px !important;
        background: #e11d48 !important;
        color: white !important; 
        font-weight: bold !important;
        height: 50px;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- KHỞI TẠO AI ---
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("🔑 Thiếu API Key trong Secrets!")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

def call_ai_v25(prompt_text):
    try:
        logic_prompt = f"[CORE 2.5] {prompt_text}"
        response = model.generate_content(logic_prompt)
        return response.text
    except Exception as e:
        if "429" in str(e):
            st.warning("⏳ Hệ thống đang nghỉ 30s để nạp lại năng lượng...")
            time.sleep(5)
            return "Vui lòng đợi một chút rồi nhấn lại nhé!"
        return f"Lỗi: {str(e)}"

# --- HEADER ---
st.markdown("<h1 class='main-title'>VĂN HIẾN AI <span class='badge-25'>2.5 PRO</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Hệ sinh thái phân tích Ngữ Văn thế hệ mới</p>", unsafe_allow_html=True)

# --- TABS NỘI DUNG ---
t1, t2, t3 = st.tabs(["📝 LẬP DÀN Ý", "🕵️ CHẤM ĐIỂM", "📡 DẪN CHỨNG"])

with t1:
    st.markdown("### 🖋️ Nhập đề bài
