import os
from dotenv import load_dotenv
import streamlit as st
import sys
import openai
from google.auth import default, transport

load_dotenv()

PROJECT_ID = "sesac-24-101"  # @param {type:"string"}
LOCATION = "us-central1"  # @param {type:"string"}

credentials, _ = default()
auth_request = transport.requests.Request()
credentials.refresh(auth_request)

client = openai.OpenAI(
    base_url=f"https://{LOCATION}-aiplatform.googleapis.com/v1beta1/projects/{PROJECT_ID}/locations/{LOCATION}/endpoints/openapi",
    api_key=credentials.token,
)

MODEL_ID = "google/gemini-1.5-flash"  # @param {type:"string"}

def generate_recipe(input):
  response = client.chat.completions.create(
      model=MODEL_ID, messages=[{"role": "generate a recipe for the following ingredient:", "content": input}]
  )

# Streamlit app layout
st.title("Recipe Generation with Gemini AI")
# Prompt input
prompt_input = st.text_area("Enter your recipe prompt", "ramen")

# Generate content on button click
if st.button("Generate Recipe"):
  # Generate the response
  try:
      response = generate_recipe(prompt_input)
      if response and 'content' in response:
        st.write(response['content'])
  except Exception as e:
      st.error(f"Error generating content: {e}")