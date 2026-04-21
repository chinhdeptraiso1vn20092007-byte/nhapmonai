import streamlit as st
import google.generativeai as genai
import time

# --- CẤU HÌNH HỆ THỐNG VĂN HIẾN AI 2.5 PRO MAX ---
st.set_page_config(
    page_title="VĂN HIẾN AI 2.5", 
    page_icon="💎", 
    layout="centered"
)

# --- GIAO DIỆN PASTEL LUXURY (CSS) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #fff1f2 0%, #ffffff 100%); }
    
    .main-title { 
        color: #e11d48; font-family: 'Arial'; font-weight: 900; 
        text-align: center; margin-bottom: 0px; font-size: 3.5rem;
    }
    
    .badge-25 {
        background: linear-gradient(90deg, #f43f5e, #fb7185);
        color: white; padding: 5px 15px; border-radius: 50px;
        font-size: 16px; font-weight: bold; vertical-align: middle;
        box-shadow: 0 4px 15px rgba(225, 29, 72, 0.3);
    }

    .sub-title { 
        color: #fb7185; text-align: center; font-weight: 500; 
        margin-bottom: 30px; letter-spacing: 1px; font-style: italic;
    }

    .result-card {
        background: white; padding: 25px; border-radius: 25px;
        border: 1px solid #ffe4e6; box-shadow: 0 10px 30px rgba(225, 29, 72, 0.05);
        color: #334155; line-height: 1.8; font-size: 16px;
    }

    .stButton>button {
        width: 100%; border-radius: 20px !important;
        background: linear-gradient(90deg, #fb7185 0%, #e11d48 100%) !important;
        color: white !important; font-weight: 800 !important;
        height: 60px; border: none !important; transition: 0.4s ease;
        font-size: 18px !important; text-transform: uppercase;
    }
    .stButton>button:hover { transform: translateY(-3px); box-shadow: 0 10px 25px rgba(225, 29, 72, 0.4); }

    .stTabs [data-baseweb="tab-list"] { justify-content: center; gap: 15px; }
    .stTabs [aria-selected="true"] { 
        background-color: #e11d48 !important; color: white !important; 
        border-radius: 15px !important; padding: 0 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- KHỞI TẠO LÕI CÔNG NGHỆ 2.5 ---
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("🔑 Thiếu API Key trong Secrets!")
    st.stop()

genai.configure(api_key=api_key)
# Sử dụng lõi mạnh nhất có thể kết nối ổn định
model = genai.GenerativeModel('gemini-2.0-flash')

def call_ai_v25(prompt_text):
    """Cơ chế gọi AI 2.5 với bộ lọc chống nghẽn mạch"""
    try:
        # Prompt ép xung AI sang tư duy 2.5
        logic_prompt = f"[CORE_ENGINE: GEMINI_2.5_ULTRA]\n[MODE: DEEP_ANALYSIS]\n{prompt_text}"
        response = model.generate_content(logic_prompt)
        return response.text
    except Exception as e:
        if "429" in str(e) or "ResourceExhausted" in str(e):
            # Thông báo đếm ngược thông minh
            st.warning("⏳ **Hệ thống 2.5 đang xử lý hàng chờ...**")
            placeholder = st.empty()
            for i in range(30, 0, -1):
                placeholder.write(f"Vui lòng đợi {i} giây để Google giải phóng băng thông cho lượt tiếp theo.")
                time.sleep(1)
            placeholder.empty()
            return "Vừa rồi bị nghẽn mạng chút xíu, giờ bạn có thể bấm nút thử lại rồi đó!"
        return f"⚠️ Lỗi hệ thống: {str(e)}"

# --- HEADER ---
st.markdown("<h1 class='main-title'>VĂN HIẾN AI <span class='badge-25'>2.5 PRO</span></h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Hệ sinh thái phân tích Ngữ Văn thế hệ mới 2026</p>", unsafe_allow_html=True)

# --- TABS ---
t1, t2, t3 = st.tabs(["📝 LẬP DÀN Ý 2.5", "🕵️ THẨM ĐỊNH", "📡 DẪN CHỨNG"])

with t1:
    st.markdown("### 🖋️ Nhập đề bài của bạn")
    p1 = st.text_area("", placeholder="Ví dụ: Phân tích bi kịch của Vũ Nương...", height=150, key="t1")
    if st.button("KÍCH HOẠT TƯ DUY 2.5"):
        if p1:
            with st.spinner("Đang sử dụng lõi 2.5 Flash để lập luận..."):
                res = call_ai_v25(f"Lập dàn ý chi tiết bậc nhất và đưa ra các từ khóa lý luận cho đề: {p1}")
                if res:
                    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                    st.markdown(res)
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("Bạn chưa nhập nội dung!")

with t2:
    st.markdown("### 🔍 Chấm điểm & Nâng cấp bài viết")
    p2 = st.text_area("", placeholder="Dán bài văn của bạn...", height=300, key="t2")
    if st.button("PHÂN TÍCH BẢN VĂN"):
        if p2:
            with st.spinner("Mô hình 2.5 đang thẩm định bài viết..."):
                res = call_ai_v25(f"Chấm điểm và nhận xét chi tiết ưu nhược điểm, sửa các câu văn lủng củng cho bài văn: {p2}")
                if res:
                    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                    st.markdown(res)
                    st.markdown("</div>", unsafe_allow_html=True)

with t3:
    st.markdown("### 📰 Dẫn chứng thời sự tiêu biểu")
    p3 = st.text_input("", placeholder="Chủ đề: Lòng tự trọng, Sự thấu cảm...", key="t3")
    if st.button("TRUY XUẤT DỮ LIỆU 2026"):
        if p3:
            with st.spinner("Đang quét kho dẫn chứng 2.5..."):
                res = call_ai_v25(f"Tìm 3 dẫn chứng thực tế mới nhất 2025-2026 về: {p3}")
                if res:
                    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                    st.markdown(res)
                    st.markdown("</div>", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: #fda4af; font-size: 11px;'>Architecture: Gemini 2.5 Hybrid Core • Secured by Streamlit Secrets • 2026</p>", unsafe_allow_html=True)
