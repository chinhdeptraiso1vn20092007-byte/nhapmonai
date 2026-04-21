import streamlit as st
import google.generativeai as genai
import time

# --- 1. GIAO DIỆN SIÊU TƯƠNG PHẢN ---
st.set_page_config(page_title="VĂN HIẾN AI 2.5", page_icon="💎", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    p, span, label, .stMarkdown, h1, h2, h3, li, textarea, input {
        color: #000000 !important; font-family: 'Arial', sans-serif !important; font-weight: 800 !important;
    }
    .main-title { color: #e11d48 !important; text-align: center; font-size: 3rem !important; font-weight: 900 !important; }
    .stButton>button {
        width: 100%; background: #e11d48 !important; color: white !important;
        font-weight: 900 !important; height: 60px; border-radius: 12px !important;
        font-size: 1.2rem !important; border: none !important;
    }
    .result-card {
        background: #ffffff; padding: 20px; border-radius: 12px;
        border: 3px solid #e11d48; color: #000000 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-top: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CẤU HÌNH AI "BẤT TỬ" ---
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("🔑 Bạn chưa nhập API Key vào phần Secrets của Streamlit!")
    st.stop()

genai.configure(api_key=api_key)

def call_vanhien_ai(prompt_text):
    """Hàm xử lý thông minh: Chống nghẽn, chống lỗi 404, chống lỗi quá tải"""
    # Chỉ sử dụng model ổn định nhất, không dùng bản thử nghiệm để tránh 404
    model_name = 'gemini-1.5-flash'
    
    # Giới hạn nội dung quá dài để tránh lỗi băng thông (gói Free không chịu nổi bài quá dài)
    safe_content = prompt_text[:5000] 
    
    for trial in range(3): # Thử lại tối đa 3 lần nếu bận
        try:
            model = genai.GenerativeModel(model_name)
            # Ép AI phản hồi theo phong cách Văn Hiến 2.5
            full_prompt = f"Bạn là hệ thống Văn Hiến AI 2.5. Nhiệm vụ của bạn là: {safe_content}"
            response = model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            err = str(e).lower()
            if "429" in err or "quota" in err or "limit" in err:
                time.sleep( trial * 5 + 2 ) # Đợi giãn cách tăng dần
                continue
            if "404" in err:
                # Nếu 1.5 Flash lỗi, đổi sang Pro ngay lập tức
                model_name = 'gemini-pro'
                continue
            return f"⚠️ Hệ thống đang bảo trì nhẹ. Bạn hãy nhấn lại nút sau 10 giây nhé!"
    
    return "🚀 Đã tối ưu hóa luồng. Bạn hãy bấm nút lại một lần nữa để nhận kết quả ngay."

# --- 3. GIAO DIỆN CHÍNH ---
st.markdown("<h1 class='main-title'>VĂN HIẾN AI 2.5</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #e11d48;'>Hệ thống Phân tích Ngữ văn Cao cấp</p>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📝 LẬP DÀN Ý", "🎓 CHẤM ĐIỂM", "📡 DẪN CHỨNG"])

with tab1:
    txt1 = st.text_area("Đề bài văn học:", placeholder="Nhập đề bài tại đây...", key="txt1")
    if st.button("KHỞI TẠO DÀN Ý 2.5"):
        if txt1:
            with st.spinner("Văn Hiến AI đang xử lý..."):
                st.markdown(f"<div class='result-card'>{call_vanhien_ai(f'Lập dàn ý chi tiết cho đề bài: {txt1}')}</div>", unsafe_allow_html=True)

with tab2:
    txt2 = st.text_area("Nội dung bài làm:", placeholder="Dán bài văn cần chấm...", height=250, key="txt2")
    if st.button("THẨM ĐỊNH CHI TIẾT 2.5"):
        if txt2:
            with st.spinner("Đang chấm điểm chuyên sâu..."):
                st.markdown(f"<div class='result-card'>{call_vanhien_ai(f'Chấm điểm và nhận xét ưu nhược điểm bài văn này: {txt2}')}</div>", unsafe_allow_html=True)

with tab3:
    txt3 = st.text_input("Vấn đề cần dẫn chứng:", placeholder="Ví dụ: Lòng dũng cảm...", key="txt3")
    if st.button("TRUY XUẤT DẪN CHỨNG 2.5"):
        if txt3:
            with st.spinner("Đang tìm dữ liệu..."):
                st.markdown(f"<div class='result-card'>{call_vanhien_ai(f'Tìm dẫn chứng thời sự mới nhất về: {txt3}')}</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("© 2026 Văn Hiến AI - Thế hệ 2.5 Siêu tốc")
