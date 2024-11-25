import os
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def upload_to_gemini(path, mime_type=None):
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

# TODO Make these files available on the local file system
# You may need to update the file paths
files = [
  upload_to_gemini("1FHRaMhwVH0jxz9fgJjR1nCT1AEnj_vtd", mime_type="application/octet-stream"),
  upload_to_gemini("1GwF-evl8fJFdC4tu4l_61OiiV_ZC6YYf", mime_type="application/octet-stream"),
]

response = model.generate_content([
  "input: ",
  files[0],
  "output: 메뉴 : 라면\n1. 재료라면 1봉지스프 1/2개대파 1뿌리올리브유 2스푼 \n\n2. 조리순서\n1. 평소대로 물을 550ml 넣고 끓여주세요 \n2. 끓는 물에 라면과 스프를 넣어주세요 여기서 포인트는 라면을 70~80%만 익혀주시는거에요,이따가 라면 볶으면서 또 익혀줄거기 때문에 푹 익히면퍼질 수가 있어요~!포인트는 라면을 70~80%만 익히기 \n3. 살짝 덜 익은 라면 물을 버려주세요그 때 라면 국물 3~4스푼은 남겨주시고 버려주세요^^ \n4. 이제 팬에 올리브유 or 식용유 2스푼을 올려주세요 \n5. 다음 아까 설익은 라면을 넣고 볶아줄거에요그리고 아까 라면 끓는 물 3~4스푼 기억나시죠?^^ \n6. 끓인 물 4스푼을 함께 넣어서 약불에서 볶아주세요~ \n7. 다음 대파를 올려주시구요~~ \n8. 대파향이 솔솔~~ 날때까지 볶아주세요저는 백종원 레시피중에 가장 마음에 드는게 대파향인거 같아요 ㅎㅎ원래 파를 좋아하기도 하지만 대파향 솔솔 나는게 참 좋아요 \n9. 다음 라면스프 1/2을 넣고 샤샤샥~ 볶아주세요10. 조금 더 넣으면 혹시 짤수가 있으니 드셔보시면서 조절하는걸로~^^ 짠~! 완성되었어요,",
  "input: ",
  files[1],
  "output: ",
])

    # Generate and display response
    st.write("Generating recipe response...")
    response_text = generate_recipe_response(files)
    st.write("Generated Recipe Response:")
    st.text(response_text)
else:
    st.write("Please upload both images to proceed.")