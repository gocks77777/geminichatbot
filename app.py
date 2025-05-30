import streamlit as st
import google.generativeai as genai

# Gemini API 키를 secrets에서 불러오기
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")
st.title("🤖 Gemini 1.5 Flash Chatbot")

# 세션 상태에 대화 이력(chat_history) 초기화
def init_chat_history():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

init_chat_history()

# Gemini 모델 준비
def get_gemini_model():
    return genai.GenerativeModel("gemini-1.5-flash")

model = get_gemini_model()

# 채팅 메시지 UI 출력
def render_chat():
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

render_chat()

# 사용자 입력 받기
user_input = st.chat_input("메시지를 입력하세요...")

if user_input:
    # 사용자 메시지 저장 및 출력
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Gemini 모델에 전체 대화 이력 전달 (최신 컨텍스트 유지)
    messages = [
        {"role": m["role"], "parts": [m["content"]]} for m in st.session_state.chat_history
    ]
    try:
        response = model.generate_content(messages)
        bot_reply = response.text.strip()
    except Exception as e:
        bot_reply = f"❗️ 오류: {e}"

    # Gemini 응답 저장 및 출력
    st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)



