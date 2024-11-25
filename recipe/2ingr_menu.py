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
    st.write(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

# Function to generate content
def generate_recipe_response(prompt_input, files):
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    # Generate content based on inputs
    response = model.generate_content([
        f"input: {prompt_input}",
        *files
    ])

    # If response is an object with a .text attribute, return response.text
    if hasattr(response, "text"):
        return response.text
    # Otherwise, return it directly
    return response

# Streamlit app layout
st.title("Recipe Generation with Gemini AI")

# Prompt input
prompt_input = st.text_area("Enter your recipe prompt", "라면")

# File uploads
uploaded_files = st.file_uploader("Upload related images (JPEG/PNG)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
files = [upload_to_gemini(file, mime_type="image/jpeg") for file in uploaded_files]

# Generate content on button click
if st.button("Generate Recipe"):
    try:
        response_text = generate_recipe_response(prompt_input, files)
        st.write(response_text)
    except Exception as e:
        st.error(f"Error generating content: {e}")
