# pip uninstall openai; pip install openai
import openai

from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
openai_model = os.getenv('OPENAI_MODEL')

client = openai.OpenAI(api_key=openai_api_key)

def ask_chatbot(user_input):
    response = client.chat.completions.create(
        model=openai_model,
        messages=[
            {'role': 'system', 'content': '당신은 나를 잘 도와주는 도우미 입니다.'},
            {'role':'user', 'content': user_input}
        ]
    )

    return response.choices[0].message.content

while True:
    user_input = input('Enter your message: ')

    if user_input.lower() in ['exit', 'quit']:
        print('대화를 종료합니다. 안녕히 가세요 👋')
        break
    if not user_input.strip():
        continue

    assistant_reply = ask_chatbot(user_input)
    print('Assistant:', assistant_reply)