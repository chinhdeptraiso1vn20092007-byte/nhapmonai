import streamlit as st
import google.generativeai as genai
import time

# --- 1. CẤU HÌNH GIAO DIỆN SIÊU TƯƠNG PHẢN (ĐEN - TRẮNG - ĐỎ) ---
st.set_page_config(page_title="VĂN HIẾN AI 2.5", page_icon="💎", layout="centered")

st.markdown("""
    <style>
    /* Nền trắng tinh để chữ đen nổi bật nhất */
    .stApp { background-color: #ffffff; }
    
    /* Ép tất cả chữ thành màu đen đậm tuyệt đối để cực kỳ dễ đọc */
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

    /* Tab bar thiết kế rõ rệt */
    .stTabs [data-baseweb="tab"] {
        background-color: #f1f5f9; border-radius: 10px; padding: 12px 25px;
        color: #000000 !important; font-weight: 800; border: 1px solid #cbd5e1;
    }
    .stTabs [aria-selected="true"] { 
        background-color: #e11d48 !important; color: white !important; 
    }

    /* Nút bấm đỏ rực, kích thước lớn, phản hồi nhanh */
    .stButton>button {
        width: 100%; background: #e11d48 !important; color: white !important;
        font-weight: 900 !important; height: 65px; border-radius: 15px !important;
        font-size: 1.3rem !important; border: none !important;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: #be123c !important;
        transform: scale(1.02);
    }

    /* Khung kết quả viền đỏ dày rành mạch */
    .result-card {
        background: #ffffff; padding: 25px; border-radius: 15px;
        border: 4px solid #e11d48; color: #000000 !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        margin-top: 20px;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. QUẢN LÝ BẢO MẬT & CẤU HÌNH AI ---
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("🔑 Thiếu API Key! Hãy kiểm tra mục Secrets trên Streamlit Cloud.")
    st.stop()

genai.configure(api_key=api_key)

def call_ai_power(content):
    """
    Chiến thuật xử lý Model:
    Sử dụng 1.5 Flash Latest để tránh lỗi 404 và đảm bảo tốc độ 'siêu tốc'.
    """
    try:
       # Sử dụng Model 2.5 Flash mới nhất
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # System Prompt ẩn để tăng chất lượng chuyên gia
        full_instruction = f"Bạn là chuyên gia Ngữ văn hệ AI 2.5. Hãy xử lý yêu cầu sau một cách chuyên nghiệp và sâu sắc: {content}"
        
        res = model.generate_content(full_instruction)
        return res.text
    except Exception as e:
        # Xử lý khi quá tải băng thông (Error 429)
        if "429" in str(e) or "ResourceExhausted" in str(e):
            time.sleep(5) # Nghỉ 5 giây để reset quota
            try:
                model_retry = genai.GenerativeModel('gemini-1.5-flash')
                res = model_retry.generate_content(content)
                return res.text
            except:
                return "⚠️ Hệ thống đang bận xử lý lưu lượng lớn. Bạn vui lòng đợi 15 giây rồi nhấn lại nút nhé!"
        return f"❌ Lỗi kết nối: {str(e)}"

# --- 3. GIAO DIỆN CHÍNH ---
st.markdown("<h1 class='main-title'>VĂN HIẾN AI 2.5</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #e11d48 !important; font-weight: bold;'>Hệ thống Phân tích Văn học Siêu tốc</p>", unsafe_allow_html=True)

# Chia Tab chức năng
t1, t2, t3 = st.tabs(["📝 DÀN Ý", "🕵️ CHẤM ĐIỂM", "📡 DẪN CHỨNG"])

with t1:
    p1 = st.text_area("Nhập đề bài văn học:", height=120, key="t1", placeholder="Ví dụ: Phân tích nhân vật Huấn Cao...")
    if st.button("LẬP DÀN Ý TỨC THÌ", key="b1"):
        if p1:
            with st.spinner("Đang kết nối siêu tốc..."):
                result = call_ai_power(f"Lập dàn ý chi tiết bài văn: {p1}")
                st.markdown(f"<div class='result-card'>{result}</div>", unsafe_allow_html=True)
        else:
            st.warning("Vui lòng nhập đề bài!")

with t2:
    p2 = st.text_area("Dán bài làm tại đây:", height=250, key="t2", placeholder="Dán nội dung bài văn của bạn...")
    if st.button("THẨM ĐỊNH NGAY", key="b2"):
        if p2:
            with st.spinner("Đang soi lỗi văn bản..."):
                result = call_ai_power(f"Hãy chấm điểm và nhận xét chi tiết ưu, nhược điểm bài văn sau: {p2}")
                st.markdown(f"<div class='result-card'>{result}</div>", unsafe_allow_html=True)
        else:
            st.warning("Vui lòng dán bài làm!")

with t3:
    p3 = st.text_input("Vấn đề xã hội:", key="t3", placeholder="Ví dụ: Sự thấu cảm, Chuyển đổi số...")
    if st.button("TÌM DẪN CHỨNG", key="b3"):
        if p3:
            with st.spinner("Đang tra cứu dữ liệu mới nhất..."):
                result = call_ai_power(f"Tìm 3 dẫn chứng thời sự mới nhất về: {p3}")
                st.markdown(f"<div class='result-card'>{result}</div>", unsafe_allow_html=True)
        else:
            st.warning("Vui lòng nhập vấn đề!")

# --- 4. FOOTER ---
st.markdown("---")
st.caption("Bản cập nhật Siêu Tương Phản & Tối Ưu Model • 2026")
