import os
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

# Configure the Gemini API key
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def generate_recipe(prompt_input):
    # Define the files variable first
    files = [
        upload_to_gemini(r"C:\Users\syoun\gcloud\recipe\ramen.jpg", mime_type="image/jpeg"),
        upload_to_gemini(r"C:\Users\syoun\gcloud\recipe\menu1.jpg", mime_type="image/jpeg"),
    ]

    # Set up generation parameters
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config
    )
    
    # Prompting the model to generate three recipes with the listed ingredients
    prompt = (
        f"Using the following ingredients: {prompt_input}, "
        "generate three unique recipes. Each recipe should include a title, ingredients list, and step-by-step instructions."
    )
    
    # Generate content based on inputs
    response = model.generate_content([
        "input: ", "라면",
        "output:", files[0], 
        """메뉴 : 라면
        
        * 재료: 
        라면 1봉지
        스프 1/2개
        대파 1뿌리
        올리브유 2스푼
        
        * 조리순서
        1. 평소대로 물을 550ml 넣고 끓여주세요 
        2. 끓는 물에 라면과 스프를 넣어주세요
        여기서 포인트는 라면을 70~80%만 익혀주시는거에요,
        이따가 라면 볶으면서 또 익혀줄거기 때문에 푹 익히면퍼질 수가 있어요~!
        포인트는 라면을 70~80%만 익히기
        3. 살짝 덜 익은 라면 물을 버려주세요그 때 라면 국물 3~4스푼은 남겨주시고 버려주세요^^
        4. 이제 팬에 올리브유 or 식용유 2스푼을 올려주세요
        5. 다음 아까 설익은 라면을 넣고 볶아줄거에요그리고 아까 라면 끓는 물 3~4스푼 기억나시죠?^^
        6. 끓인 물 4스푼을 함께 넣어서 약불에서 볶아주세요~
        7. 다음 대파를 올려주시구요~~
        8. 대파향이 솔솔~~ 날때까지 볶아주세요저는 백종원 레시피중에 가장 마음에 드는게 대파향인거 같아요 
        ㅎㅎ원래 파를 좋아하기도 하지만 대파향 솔솔 나는게 참 좋아요
        9. 다음 라면스프 1/2을 넣고 샤샤샥~ 볶아주세요
        10. 조금 더 넣으면 혹시 짤수가 있으니 드셔보시면서 조절하는걸로~^^
        
        짠~! 완성되었어요"
        """,
        
        "input: ", "제육볶음",
        "output: ", files[1],
        """	
        *메뉴: 제육볶음
        
        *재료:
          돼지고기 앞다리살 600g
          양파 1/2개
          청양고추 2~3개
          대파 1/3개 
          고추장 3큰술
          고춧가루 2큰술
          다진마늘 1큰술
          설탕 또는 매실액 2큰술
          간장 1큰술 
          통깨 약간
          후추 약간
        
        *조리순서:
1. 양념재료를 모두 넣어주세요~.	
2. 양념재료가 잘 섞이도록해주세요~.	
3. 대파와 청양고추는 어슷썰어주고 양파는 1cm 두께로 썰어주세요~.	
4. 돼지고기는 한입크기로 썰어주세요~.	
5. 만들어둔 양념장을 고기에 넣어 버무려주세요~.	
6. 양념 후 바로 볶아도 되지만 냉장고에 30분정도 두어 숙성시켜주면 양념이 베어 더욱 맛있답니다~!!	
7. 팬에 식용유 2큰술과 대파를 넣고 강불로 3분정도 볶아 파기름을 내주세요~.	
8. 양념한 고기를 넣어주세요~.	
9. 중불로 볶아 고기를 완전히 익혀주세요~.
10. 약 8분정도면 다 익는답니다~!!	
11. 양파와 청양고추를 넣어주세요~.	
12. 강불로 2분정도 볶아준뒤 불을 꺼주세요~.	
13. 마지막으로 통깨를 뿌려주면 맛있는 제육볶음 완성입니다~!!"
"""
    ])
    return response
