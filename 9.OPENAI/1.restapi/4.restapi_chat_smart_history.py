import requests

from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
openai_request_url = os.getenv('OPENAI_REQUEST_URL')
openai_model = os.getenv('OPENAI_MODEL')

message = []
message.append({'role': 'system', 'content': '너는 나를 잘 도와주는 경력 20년차의 실력이 매우 좋은 소프트웨어 개발자야.'})

def ask_chatbot(user_input, history=message):
    history.append({'role': 'user', 'content': user_input})

    try:

        response = requests.post(
            openai_request_url,
            json={
                'model': openai_model,
                'messages': history,
                'temperature': 1.0
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {openai_api_key}' # NOTE: Basic 인증 = Basic Authorization
            }
        )

        data = response.json()
        assistant_reply = data['choices'][0]['message']['content']
        history.append({'role': 'assistant', 'content': assistant_reply})

        # example: 히스토리를 20개로 제한. history = [history[0]] + history[-19:]
        if len(history) > 20:
            history = [history[0]] + history[-19:]

        return assistant_reply, history
    except Exception as e:
        print("Error:", e)
        return "죄송합니다. 답변을 생성하는 중에 오류가 발생했습니다."

while True:
    user_input = input("Enter your message: ")

    if user_input.lower() in ['exit', 'quit']:
        print('대화를 종료합니다. 안녕히 가세요 👋')
        break
    if not user_input.strip():
        continue

    assistant_reply, message = ask_chatbot(user_input)
    print("Assistant:", assistant_reply)
