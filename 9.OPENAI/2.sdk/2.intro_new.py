# pip uninstall openai; pip install openai
import openai

from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
openai_model = os.getenv('OPENAI_MODEL')

client = openai.OpenAI(api_key=openai_api_key)

response = client.chat.completions.create(
    model=openai_model,
    messages=[
        {'role': 'system', 'content': '당신은 나를 잘 도와주는 도우미 입니다.'},
        {'role':'user', 'content':'안녕하세요, 반갑습니다.'}
    ]
)

assistant_reply = response.choices[0].message.content
print("Assistant:", assistant_reply)