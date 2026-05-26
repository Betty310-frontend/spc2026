import requests

from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
openai_request_url = os.getenv('OPENAI_COMPLETIONS_URL')
openai_model = os.getenv('OPENAI_MODEL')

def ask_chatbot(user_input):
    response = requests.post(
        openai_request_url,
        json={
            'model': openai_model,
            'messages': [
                {'role': 'system', 'content': '너는 나를 잘 도와주는 경력 20년차의 실력이 매우 좋은 소프트웨어 개발자야.'},
                {'role': 'user', 'content': user_input},
            ],
            'temperature': 1.3
        },
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {openai_api_key}' # NOTE: Basic 인증 = Basic Authorization
        }
    )

    data = response.json()
    assistant_reply = data['choices'][0]['message']['content']
    return assistant_reply

while True:
    user_input = input("Enter your message: ")

    if user_input.lower() in ['exit', 'quit']:
        print('대화를 종료합니다. 안녕히 가세요 👋')
        break
    if not user_input.strip():
        continue

    assistant_reply = ask_chatbot(user_input)
    print("Assistant:", assistant_reply)
