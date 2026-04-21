import streamlit as st
import google.generativeai as genai

# 1. Cấu hình trang với giao diện rộng và icon dễ thương
st.set_page_config(
    page_title="Văn Học Trẻ - Lập Dàn Ý 2.5",
    page_icon="🌸",
    layout="wide"
)

# 2. CSS Giao diện màu hồng sinh động và icon trang trí
st.markdown("""
    <style>
    /* Nền tổng thể màu hồng nhạt */
    .stApp {
        background-color: #fff0f3;
    }
    
    /* Làm đẹp tiêu đề chính */
    .main-title {
        color: #c2185b;
        text-align: center;
        font-family: 'Lexend', sans-serif;
        font-size: 3.2rem;
        font-weight: 800;
        margin-bottom: 0px;
    }

    /* Bo góc các ô nhập liệu và đổi màu viền hồng */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 20px !important;
        border: 2px solid #f48fb1 !important;
    }

    /* Nút bấm Gradient Hồng - Cam cực đẹp */
    .stButton>button {
        background: linear-gradient(90deg, #ff4081, #f06292) !important;
        color: white !important;
        border-radius: 30px !important;
        border: none !important;
        padding: 1rem !important;
        font-size: 1.3rem !important;
        font-weight: bold !important;
        box-shadow: 0 4px 15px rgba(255, 64, 129, 0.4);
        transition: 0.3s;
        width: 100%;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(255, 64, 129, 0.6);
    }

    /* Khung hiển thị dàn ý chi tiết */
    .result-card {
        background-color: white;
        padding: 30px;
        border-radius: 30px;
        border-left: 12px solid #ff4081;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        color: #444;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Thanh bên (Sidebar) với họa tiết cây bút và sách
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #c2185b;'>📚 Góc Sáng Tạo</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/5903/5903939.png", width=150)
    st.write("---")
    st.markdown("✨ **Thành viên:** Khang - Sư phạm Ngữ văn")
    st.markdown("🖍️ **Công cụ:** Gemini 2.5 Flash")
    st.image("https://cdn-icons-png.flaticon.com/512/2641/2641409.png", width=100)

# 4. Tiêu đề trang trí
st.markdown('<h1 class="main-title">🌸 TRÌNH LẬP DÀN Ý VĂN HỌC 🌸</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #ad1457;'>✨ Nơi biến ngữ liệu thành những ý tưởng tuyệt vời ✨</p>", unsafe_allow_html=True)

# 5. Kết nối API & Model 2.5
try:
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Chưa cấu hình API Key trong Secrets!")
    else:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # Ép sử dụng model 2.5 Flash
        model = genai.GenerativeModel('gemini-2.5-flash')

        # Giao diện chính
        col1, col2 = st.columns([1, 1], gap="large")

        with col1:
            st.markdown("### 🖋️ Nhập Đề Bài")
            topic = st.text_input("", placeholder="Nhập đề bài văn tại đây...")
            
            st.markdown("### 📖 Cung Cấp Ngữ Liệu")
            context = st.text_area("", height=300, placeholder="Dán đoạn văn, bài thơ hoặc thông tin cần phân tích...")

        with col2:
            st.markdown("### 🚀 Phân Tích & Lập Dàn Ý")
            st.write("Nhấn nút bên dưới để AI 2.5 giúp bạn xây dựng bộ khung cho bài viết nhé!")
            
            if st.button("💝 Bắt Đầu Lập Dàn Ý"):
                if topic and context:
                    with st.spinner('💖 Đang đọc hiểu ngữ liệu bằng trí tuệ nhân tạo 2.5...'):
                        prompt = f"""
                        Bạn là một giáo viên dạy văn giỏi. Hãy phân tích ngữ liệu sau và lập dàn ý chi tiết cho đề bài.
                        Đề bài: {topic}
                        Ngữ liệu: {context}
                        
                        Yêu cầu trình bày dàn ý:
                        1. Mở bài: Dẫn dắt ấn tượng.
                        2. Thân bài: Chia rõ các luận điểm, mỗi luận điểm có dẫn chứng từ ngữ liệu.
                        3. Đánh giá nghệ thuật: Chỉ ra nét đặc sắc trong ngữ liệu.
                        4. Kết bài: Tổng kết và liên hệ bản thân.
                        Sử dụng các emoji (📚, ✨, ✍️, 📌) để dàn ý sinh động.
                        """
                        
                        response = model.generate_content(prompt)
                        st.success("Tada! Dàn ý của bạn đã xong nè! ✨")
                        st.markdown(f'<div class="result-box result-card">{response.text}</div>', unsafe_allow_html=True)
                        st.balloons()
                else:
                    st.warning("Khang ơi, nhớ điền đủ cả Đề bài và Ngữ liệu nha! 🌸")

except Exception as e:
    st.error(f"Hệ thống gặp chút sự cố: {e}")
