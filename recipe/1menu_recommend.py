import os
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Function to generate recipes
def generate_recipes(ingredients):
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 1500,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    # Prompting the model to generate three recipes with the listed ingredients
    prompt = (
        f"Using the following ingredients: {ingredients}, "
        "generate three unique recipes. Each recipe should include a title, ingredients list, and step-by-step instructions."
    )

    response = model.generate_content([prompt])

    # Return response content if it exists
    if hasattr(response, "text"):
        return response.text
    return response

# Streamlit app layout
st.title("Recipe Generator with Gemini AI")
st.write("Enter a list of ingredients, and I’ll generate three unique recipes for you!")

# User input for ingredients
ingredients_input = st.text_area("List your ingredients (e.g., chicken, garlic, rice)", "chicken, garlic, rice")

# Generate content on button click
if st.button("Generate Recipes"):
    try:
        # Generate recipes based on the ingredients input
        recipes = generate_recipes(ingredients_input)
        st.write(recipes)
    except Exception as e:
        st.error(f"Error generating recipes: {e}")
