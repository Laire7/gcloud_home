import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Function to upload a file to Gemini
def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini."""
    file = genai.upload_file(path, mime_type=mime_type)
    st.write(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

# Model configuration for generation
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Set up the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Streamlit UI
st.title("Gemini AI Recipe Generator")

# Prompt input
prompt_input = st.text_area("Enter your recipe prompt", "라면")

# Generate content on button click
if st.button("Generate Recipe"):
        # Create the input for Gemini
        input_list = [
            f"input: {prompt_input}",
            "output:"
        ]

        # Generate the response
        try:
            response = model.generate_content(input_list)
            st.write(response.text)
        except Exception as e:
            st.error(f"Error generating content: {e}")
