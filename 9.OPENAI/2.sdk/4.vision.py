# pip uninstall openai; pip install openai
import openai

from dotenv import load_dotenv
import os, base64

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
openai_model = os.getenv('OPENAI_MODEL')

client = openai.OpenAI(api_key=openai_api_key)

def encode_image_to_base64(image_path):
    # 이미지를 읽어서 base64로 인코딩하는 함수
    with open(image_path, "rb") as file:
        base64_bytes = base64.b64encode(file.read()).decode('utf-8')
        return f"data:image/jpeg;base64,{base64_bytes}"

def ask_chatbot(user_input, image_path):
    image_base64 = encode_image_to_base64(image_path)

    response = client.chat.completions.create(
        model=openai_model,
        messages=[
            {'role': 'system', 'content': '당신은 스포츠 심사위원 입니다.'},
            {'role':'user', 'content': [
                {"type": "text", "text": user_input}, 
                {
                    "type": "image_url", 
                    "image_url": {
                        "url": image_base64
                    }
                }
            ]}
        ]
    )

    return response.choices[0].message.content

while True:
    user_input = input('Enter your message: ') or '나의 스쿼트 자세가 어떤지 전문가 입장에서 피드백을 주세요. 그리고 10점 만점 기준으로 냉정하게 점수를 주세요.'

    if user_input.lower() in ['exit', 'quit']:
        print('대화를 종료합니다. 안녕히 가세요 👋')
        break
    if not user_input.strip():
        continue

    image_path = input('Enter the image path: ') or 'squats_bad.jpg'

    assistant_reply = ask_chatbot(user_input, image_path)
    print('Assistant:', assistant_reply)

# image_path="dog.jpg"
# question="이 사진에 있는 동물은 몇 마리인가요?"
# print(ask_chatbot(question, image_path))