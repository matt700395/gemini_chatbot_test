import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Check if API key exists
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ Gemini API 키가 설정되지 않았습니다. .streamlit/secrets.toml 파일에 GOOGLE_API_KEY를 설정해주세요.")
    st.stop()

# Configure Gemini API
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"⚠️ Gemini API 초기화 중 오류가 발생했습니다: {str(e)}")
    st.stop()

# Set page config
st.set_page_config(
    page_title="Gemini 챗봇",
    page_icon="🤖",
    layout="centered"
)

# Title and description
st.title("🤖 Gemini 챗봇")
st.markdown("Gemini API를 활용한 기본 챗봇 프레임워크입니다.")

# Initialize session state for chat and chat history
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history in expander
with st.expander("이전 대화 보기", expanded=False):
    if not st.session_state.chat_history:
        st.info("아직 대화 내용이 없습니다.")
    else:
        for i, message in enumerate(st.session_state.chat_history):
            if message["role"] == "user":
                st.markdown(f"**사용자 {i//2 + 1}**: {message['content']}")
            else:
                st.markdown(f"**Gemini {i//2 + 1}**: {message['content']}")
            st.divider()

# Display current chat
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("메시지를 입력하세요..."):
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        try:
            # Show a spinner while generating response
            with st.spinner("응답을 생성하는 중..."):
                response = st.session_state.chat.send_message(prompt)
                st.markdown(response.text)
            
            # Add assistant response to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"⚠️ 응답 생성 중 오류가 발생했습니다: {str(e)}") 
