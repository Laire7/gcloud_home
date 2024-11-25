import os
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st
# import markdown
# import re

# Load environment variables
load_dotenv()

# Configure the Gemini API key
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# def markdown_to_plain_text(markdown_text):
#     # Remove Markdown syntax using regular expressions
#     plain_text = markdown_text
#     plain_text = re.sub(r'#.*', '', plain_text)  # Remove headers
#     plain_text = re.sub(r'\*\*(.*?)\*\*', r'\1', plain_text)  # Remove bold
#     plain_text = re.sub(r'\*(.*?)\*', r'\1', plain_text)  # Remove italics
#     plain_text = re.sub(r'!\[.*?\]\(.*?\)', '', plain_text)  # Remove images
#     plain_text = re.sub(r'\[.*?\]\(.*?\)', '', plain_text)  # Remove links
#     plain_text = re.sub(r'[-*] ', '', plain_text)  # Remove bullet points
#     plain_text = re.sub(r'`(.*?)`', r'\1', plain_text)  # Remove inline code
#     plain_text = re.sub(r'> ', '', plain_text)  # Remove blockquotes
#     return plain_text.strip()

def upload_to_gemini(path, mime_type=None):
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

def generate_recipe(prompt_input):
    # Set up generation parameters
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    
    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config)
    
    # Prompting the model to generate three recipes with the listed ingredients
    prompt = (
        f"Using the following ingredients: {prompt_input}, "
        "generate three unique recipes. Each recipe should include a title, ingredients list, and step-by-step instructions."
    )
    
        # Generate content based on inputs
    response = model.generate_content([prompt])
    return response

# Streamlit app layout
st.title("Recipe Generation with Gemini AI")

# Prompt input
prompt_input = st.text_area("Enter your recipe prompt", "ramen")

# Generate content on button click
if st.button("Generate Recipe"):
    # Generate the response
    try:
        response = generate_recipe(prompt_input)
        if response:
            # Parse and display the generated recipes
            generated_content = str(response.candidates[0].content.parts[0])
            recipes = generated_content.split("\n\n")  # Assume recipes are separated by double newlines
            
            for idx, recipe in enumerate(recipes, start=1):
                st.subheader(f"Recipe {idx}")
                st.write(recipe)

                # Generate a placeholder image link or display a generic one
                # Replace this with actual AI-generated images when supported
                st.image(f"https://via.placeholder.com/600x400?text=Recipe+{idx}+Image", caption=f"Image for Recipe {idx}")
        else:
            st.error("No content generated. Please try again with a different prompt.")
    except Exception as e:
        st.error(f"Error generating content: {e}")
