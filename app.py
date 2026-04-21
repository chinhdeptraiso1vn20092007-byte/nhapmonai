import streamlit as st
import google.generativeai as genai

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="VĂN HIẾN AI 3.5", page_icon="📖", layout="centered")

# --- PHONG CÁCH GIAO DIỆN (CUSTOM CSS) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #fff1f2 0%, #fff5f5 100%); }
    .main-title { color: #e11d48; font-family: 'Inter', sans-serif; font-weight: 800; text-align: center; margin-bottom: 5px; }
    .sub-title { color: #fb7185; text-align: center; font-weight: 500; margin-bottom: 30px; }
    .stTextArea textarea, .stTextInput input { border-radius: 20px !important; border: 1px solid #fecdd3 !important; padding: 15px !important; }
    .stButton>button {
        width: 100%; border-radius: 15px !important;
        background: linear-gradient(90deg, #fb7185 0%, #e11d48 100%) !important;
        color: white !important; font-weight: 700 !important; padding: 12px 0px !important; border: none !important;
        transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(225, 29, 72, 0.2);
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(225, 29, 72, 0.3); }
    .result-container { background-color: white; padding: 25px; border-radius: 25px; border: 1px solid #ffe4e6; box-shadow: 0 10px 30px rgba(0,0,0,0.05); margin-top: 20px; }
    .stTabs [data-baseweb="tab-list"] { justify-content: center; gap: 8px; }
    .stTabs [aria-selected="true"] { background-color: #e11d48 !important; color: white !important; border-radius: 12px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- BẢO MẬT API KEY ---
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("❌ Thiếu API Key trong phần Secrets!")
    st.stop()

genai.configure(api_key=api_key)

# Cấu hình mô hình mạnh nhất (Experimental / Thinking Mode) 
# Lưu ý: 'gemini-2.0-flash-thinking-exp' là bản có khả năng suy luận sâu nhất hiện tại
model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp')

# --- HEADER ---
st.markdown("<h1 class='main-title'>VĂN HIẾN AI 3.5</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Hệ sinh thái học văn cao cấp (Model 2.5 Hybrid)</p>", unsafe_allow_html=True)

# --- TABS NỘI DUNG ---
tab1, tab2, tab3 = st.tabs(["📝 Lập Dàn Ý", "🕵️ Chấm Điểm", "💡 Dẫn Chứng"])

def generate_ai_response(prompt_text):
    try:
        # Sử dụng chế độ stream để nội dung hiện ra mượt hơn
        response = model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        return f"Lỗi kết nối mô hình: {str(e)}. Thử lại sau."

with tab1:
    st.markdown("### 🖋️ Nhập đề bài văn học")
    prompt = st.text_area("", placeholder="Ví dụ: Phân tích tâm trạng bà cụ Tứ...", height=150, key="p1")
    if st.button("TẠO DÀN Ý CHUYÊN SÂU"):
        if prompt:
            with st.spinner("Đang sử dụng trí tuệ nhân tạo thế hệ mới..."):
                res = generate_ai_response(f"Bạn là chuyên gia Ngữ Văn bậc nhất. Hãy lập dàn ý cực kỳ chi tiết, kèm các nhận định văn học đắt giá cho đề bài: {prompt}")
                st.markdown("<div class='result-container'>", unsafe_allow_html=True)
                st.markdown(res)
                st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("### 🔍 Phân tích & Chấm điểm")
    essay = st.text_area("", placeholder="Dán bài làm của bạn...", height=300, key="p2")
    if st.button("BẮT ĐẦU THẨM ĐỊNH"):
        if essay:
            with st.spinner("Đang quét lỗi logic và diễn đạt..."):
                res = generate_ai_response(f"Hãy chấm điểm bài viết này trên thang điểm 10 theo tiêu chí thi THPTQG. Phân tích sâu các lỗi sai và gợi ý cách sửa chuyên nghiệp: {essay}")
                st.markdown("<div class='result-container'>", unsafe_allow_html=True)
                st.markdown(res)
                st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    st.markdown("### 📰 Dẫn chứng thời sự thực tế")
    topic = st.text_input("", placeholder="Chủ đề (VD: Sự tử tế, Chuyển đổi số...)", key="p3")
    if st.button("TRUY XUẤT DẪN CHỨNG"):
        if topic:
            with st.spinner("Đang tìm dữ liệu mới nhất 2026..."):
                res = generate_ai_response(f"Cung cấp 3 dẫn chứng sự kiện/nhân vật có thật trong 1 năm gần đây về {topic}. Phân tích ý nghĩa dẫn chứng.")
                st.markdown("<div class='result-container'>", unsafe_allow_html=True)
                st.markdown(res)
                st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br><hr><p style='text-align: center; color: #fda4af;'>Dành riêng cho sĩ tử • Phiên bản 2.5 Experimental • 2026</p>", unsafe_allow_html=True)
