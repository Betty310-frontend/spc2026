import requests

from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
openai_request_url = os.getenv('OPENAI_REQUEST_URL')
openai_model = os.getenv('OPENAI_MODEL')

user_input = input("Enter your message: ") or '강아지를 데려왔어. 강아지 이름을 뭐라고 지을까?'

response = requests.post(
    openai_request_url,
    json={
        'model': openai_model,
        'messages': [
            {'role': 'system', 'content': '너는 나를 잘 도와주는 경력 20년차의 실력이 매우 좋은 작명가야.'},
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
print("Assistant:", assistant_reply)