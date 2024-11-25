# emoji : https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
# st_chatbot.py
import google.generativeai as genai 
import streamlit as st
from dotenv import load_dotenv
import os

# Create the model
# 모델의 설정
generation_config = {
    # 온도가 올라가면 예측이 어려지고, 낮으면 쉬워진다.(확률분포를 조정)
    "temperature": 1,
    # 확률분포 내에서 선택할 단어의 범위를 결정하는 매개변수
    "top_p": 0.95,
    # 확률분포 내에서 선택할 단어의 수를 결정하는 매개변수
    "top_k": 64,
    # 응답하는 메시지의 최대 토큰 수
    "max_output_tokens": 8192,
    # 응답하는 메시지의 데이터 타입
    "response_mime_type": "text/plain",
}

# 설정 
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.title("Gemini-Bot")

@st.cache_resource
def load_model():
    model = genai.GenerativeModel('gemini-1.5-flash',
            generation_config=generation_config)
    print("model loaded...")
    return model

model = load_model()

# streamlit에서 chat사용시 history관리를 해줘야 한다.
if "chat_session" not in st.session_state:    
    st.session_state["chat_session"] = model.start_chat(history=[]) 

# 과거 채팅 메시지를 출력 + 화면 업데이트시에 새로 출력
for content in st.session_state.chat_session.history:
    with st.chat_message("ai" if content.role == "model" else "user"):
        st.markdown(content.parts[0].text)

if prompt := st.chat_input("메시지를 입력하세요."):    
    with st.chat_message("user", avatar="C:/Users/park0/gcloud/data/dog.png"):
        st.markdown(prompt)
    with st.chat_message("ai", avatar="😂"):
        response = st.session_state.chat_session.send_message(prompt)        
        st.markdown(response.text)