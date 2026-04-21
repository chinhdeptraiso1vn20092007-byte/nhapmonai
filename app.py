import streamlit as st
import google.generativeai as genai

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="VĂN HIẾN AI 3.5", page_icon="📖", layout="wide")

# --- PHONG CÁCH PASTEL (CSS) ---
st.markdown("""
    <style>
    @keyframes bounce-slow {
        0%, 100% { transform: translateY(-5%); }
        50% { transform: translateY(0); }
    }
    .stApp { background-color: #fff1f2; }
    .stButton>button {
        background-color: #f43f5e; color: white; border-radius: 20px;
        padding: 10px 25px; border: none; font-weight: bold; width: 100%;
    }
    .animate-bounce-slow { animation: bounce-slow 4s infinite ease-in-out; }
    .stTextArea>div>div>textarea { border-radius: 15px; border: 2px solid #fecdd3; }
    h1 { color: #e11d48; font-family: 'Arial'; }
    </style>
    """, unsafe_allow_html=True)

# --- BẢO MẬT API KEY ---
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.warning("⚠️ Vui lòng cấu hình GEMINI_API_KEY trong phần Secrets của Streamlit Cloud.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- GIAO DIỆN ---
st.markdown("<h1 style='text-align: center;'>VĂN HIẾN AI 3.5 📖</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #fb7185;'>Hệ sinh thái học văn Pastel</p>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📝 Dàn ý", "🕵️ Chấm điểm", "📰 Dẫn chứng"])

with tab1:
    prompt = st.text_area("Nhập đề bài văn học:", placeholder="Ví dụ: Phân tích nhân vật Tràng trong tác phẩm Vợ nhặt...", key="outline_input")
    if st.button("Lập dàn ý ngay"):
        if prompt:
            with st.spinner("Đang tư duy..."):
                try:
                    response = model.generate_content(f"Bạn là giáo viên Văn. Hãy lập dàn ý chi tiết cho đề bài: {prompt}")
                    st.markdown("### ✨ Kết quả dàn ý:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Lỗi: {e}")
        else:
            st.error("Vui lòng nhập đề bài!")

with tab2:
    essay = st.text_area("Dán bài viết của bạn:", height=300, key="eval_input")
    if st.button("Chấm điểm & Nhận xét"):
        if essay:
            with st.spinner("Đang đọc bài..."):
                response = model.generate_content(f"Bạn là chuyên gia chấm thi Ngữ văn. Hãy nhận xét ưu nhược điểm và gợi ý nâng cấp bài viết sau: {essay}")
                st.write(response.text)
        else:
            st.error("Vui lòng dán bài làm!")

with tab3:
    topic = st.text_input("Nhập vấn đề xã hội:", placeholder="Ví dụ: Lòng trắc ẩn, Sự thấu cảm...", key="news_input")
    if st.button("Tìm dẫn chứng"):
        if topic:
            with st.spinner("Đang tìm dữ liệu..."):
                response = model.generate_content(f"Cung cấp 3 dẫn chứng thời sự mới nhất về: {topic}")
                st.write(response.text)
        else:
            st.error("Vui lòng nhập chủ đề!")
