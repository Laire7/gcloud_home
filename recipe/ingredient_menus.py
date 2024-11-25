import os
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Function to upload a file to Gemini
def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini."""
    file = genai.upload_file(path, mime_type=mime_type)
    return file

# Function to generate content
def generate_recipe_response(text):
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 20,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    HOME = os.getcwd() 
    # Generate content based on inputs
    response = model.generate_content([
        "input: 계란", 
        "output: ", 
        upload_to_gemini( os.path.join(HOME,'egg_toast.jpg'), mime_type="image/jpeg" ),
        """
        1. 계란 토스트
재료: 계란, 식빵, 소금, 후추, 버터, 좋아하는 토핑 (베이컨, 치즈 등)
만드는 법:
식빵에 버터를 바르고 후라이팬에 구워줍니다.
볼에 계란을 깨고 소금, 후추로 간을 합니다.
식빵 위에 계란물을 부어 노릇하게 익혀줍니다.
좋아하는 토핑을 추가하여 맛있게 즐깁니다.
""",
upload_to_gemini( os.path.join(HOME,'egg_fried_rice.jpg'), mime_type="image/jpeg"),
"""
2. 계란 볶음밥
재료: 계란, 밥, 김치, 파, 소금, 식용유
만드는 법:
달군 팬에 식용유를 두르고 김치와 파를 볶아줍니다.
밥을 넣고 함께 볶다가 계란을 풀어 넣어 스크램블 에그처럼 볶아줍니다.
소금으로 간을 하고 참기름을 넣어 마무리합니다.
""",
upload_to_gemini( os.path.join(HOME,'egg_omelet.png'), mime_type="image/png"),
"""
3. 오믈렛
재료: 계란, 우유, 소금, 후추, 좋아하는 채소 (피망, 양파 등)
만드는 법:
계란에 우유, 소금, 후추를 넣고 잘 섞어줍니다.
채소를 볶아 계란물에 넣어줍니다.
달군 팬에 식용유를 두르고 계란물을 부어 천천히 익혀줍니다.
한쪽 끝부터 돌돌 말아줍니다.
"""
    ])

    return response.text

# Streamlit app layout
st.title("Recipe Generation with Gemini AI")
# Prompt input
prompt_input = st.text_area("Enter your recipe prompt", "라면")

# Generate content on button click
if st.button("Generate Recipe"):
    # Generate the response
    try:
        response = generate_recipe_response(prompt_input)
        st.write(response.text)
    except Exception as e:
        st.error(f"Error generating content: {e}")