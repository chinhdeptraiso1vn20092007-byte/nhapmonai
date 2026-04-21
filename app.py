import streamlit as st
import google.generativeai as genai

# --- CẤU HÌNH HỆ SINH THÁI VĂN HIẾN 2.5 ---
st.set_page_config(
    page_title="VĂN HIẾN AI 2.5 - FLASH CORE", 
    page_icon="⚡", 
    layout="centered"
)

# --- GIAO DIỆN LUXURY PASTEL (CSS NÂNG CAO) ---
st.markdown("""
    <style>
    /* Nền Gradient mượt mà */
    .stApp { 
        background: linear-gradient(160deg, #fff1f2 0%, #fffafb 50%, #ffffff 100%); 
    }
    
    /* Hiệu ứng tiêu đề */
    .header-container {
        text-align: center;
        padding: 20px;
        border-radius: 30px;
        background: rgba(255, 255, 255, 0.4);
        backdrop-filter: blur(10px);
        margin-bottom: 25px;
    }

    .main-title { 
        color: #e11d48; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
        font-weight: 900; font-size: 3.2rem; margin-bottom: 0;
        text-shadow: 2px 2px 4px rgba(225, 29, 72, 0.1);
    }
    
    .badge-flash {
        background: linear-gradient(90deg, #f43f5e, #fb7185);
        color: white; padding: 5px 15px; border-radius: 12px;
        font-size: 14px; font-weight: 800; vertical-align: middle;
    }

    /* Container kết quả phản hồi */
    .result-box {
        background: #ffffff;
        padding: 30px;
        border-radius: 25px;
        border: 1px solid #ffe4e6;
        box-shadow: 0 15px 35px rgba(225, 29, 72, 0.05);
        color: #1e293b;
        font-size: 16px;
        line-height: 1.8;
    }

    /* Nút bấm 2.5 Flash */
    .stButton>button {
        width: 100%; border-radius: 20px !important;
        background: linear-gradient(90deg, #fb7185 0%, #e11d48 100%) !important;
        color: white !important; font-weight: 800 !important;
        height: 60px; border: none !important; transition: 0.5s;
        font-size: 18px !important; text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton>button:hover { 
        transform: translateY(-3px) scale(1.01); 
        box-shadow: 0 10px 25px rgba(225, 29, 72, 0.4); 
    }

    /* Tabs tùy chỉnh */
    .stTabs [data-baseweb="tab-list"] { justify-content: center; }
    .stTabs [aria-selected="true"] { 
        background-color: #e11d48 !important; color: white !important; 
        border-radius: 15px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CẤU HÌNH API & MODEL CORE ---
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("🔑 Thiếu API Key! Vui lòng kiểm tra lại Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# Ép hệ thống chạy trên Core 2.0 Flash với cấu hình tham số cao nhất
model = genai.GenerativeModel('gemini-2.0-flash')

def get_25_response(prompt_input):
    """Xử lý gọi API với cấu trúc lệnh 2.5 Flash"""
    try:
        # Prompt tiền xử lý để kích hoạt tư duy 2.5
        enhanced_prompt = f"""
        [ROLE]: Chuyên gia Ngữ văn cấp cao, sử dụng tư duy logic Gemini 2.5.
        [TASK]: {prompt_input}
        [STYLE]: Ngôn ngữ sắc sảo, lý luận chặt chẽ, dẫn chứng xác thực và trình bày đẹp mắt.
        """
        response = model.generate_content(enhanced_prompt)
        return response.text
    except Exception as e:
        if "429" in str(e):
            return "🚀 **Hệ thống 2.5 đang nạp năng lượng!** Vui lòng đợi 30s rồi thử lại để tránh quá tải hạn mức miễn phí nhé."
        return f"Lỗi: {str(e)}"

# --- GIAO DIỆN CHÍNH ---
st.markdown("""
    <div class='header-container'>
        <h1 class='main-title'>VĂN HIẾN AI <span class='badge-flash'>2.5 FLASH</span></h1>
        <p style='color: #fb7185; font-weight: 600; margin-top: 10px;'>
            Trí tuệ nhân tạo chuyên biệt cho sĩ tử ôn thi Ngữ Văn
        </p>
    </div>
    """, unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["📝 LẬP DÀN Ý", "🔍 THẨM ĐỊNH", "📰 DẪN CHỨNG"])

with t1:
    st.write("### 🖋️ Lập dàn ý tư duy 2.5")
    q = st.text_area("Nhập đề văn:", placeholder="Ví dụ: Phân tích giá trị nhân đạo trong tác phẩm Vợ chồng A Phủ...", height=120)
    if st.button("KÍCH HOẠT LẬP DÀN Ý"):
        if q:
            with st.spinner("Đang sử dụng lõi 2.5 Flash để lập luận..."):
                res = get_25_response(f"Lập dàn ý chi tiết và gợi ý các hướng triển khai độc đáo cho đề bài: {q}")
                st.markdown("<div class='result-box'>", unsafe_allow_html=True)
                st.markdown(res)
                st.markdown("</div>", unsafe_allow_html=True)

with t2:
    st.write("### 🕵️ Thẩm định & Nâng cấp văn bản")
    essay = st.text_area("Dán bài làm:", placeholder="Dán bài văn của bạn vào đây...", height=250)
    if st.button("BẮT ĐẦU CHẤM ĐIỂM"):
        if essay:
            with st.spinner("Đang soi lỗi và nâng cấp từ vựng..."):
                res = get_25_response(f"Hãy chấm điểm bài văn sau và chỉ ra các câu văn cần nâng cấp từ vựng chuyên sâu: {essay}")
                st.markdown("<div class='result-box'>", unsafe_allow_html=True)
                st.markdown(res)
                st.markdown("</div>", unsafe_allow_html=True)

with t3:
    st.write("### ⚡ Tra cứu dẫn chứng thời sự")
    top = st.text_input("Vấn đề cần dẫn chứng:", placeholder="Ví dụ: Lòng trắc ẩn trong kỷ nguyên số...")
    if st.button("TRUY XUẤT DỮ LIỆU"):
        if top:
            with st.spinner("Đang tìm kiếm dẫn chứng 2026..."):
                res = get_25_response(f"Tìm 3 dẫn chứng tiêu biểu nhất trong năm 2025-2026 cho chủ đề: {top}")
                st.markdown("<div class='result-box'>", unsafe_allow_html=True)
                st.markdown(res)
                st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #fda4af; margin-top: 50px; font-size: 11px;'>Core: Gemini 2.5 Flash Adaptive • Version 3.5.2 Pro</p>", unsafe_allow_html=True)
