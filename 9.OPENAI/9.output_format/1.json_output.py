import os, json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

user_input = '서울의 인구와 면적을 알려주세요.'

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {'role': 'system', 'content':'질문에 대해 json으로만 답변하시오. 답변은 항상 json 형식으로 작성되어야 합니다.'},
        {'role':'user', 'content':user_input}
    ]
)

answer = response.choices[0].message.content
print(answer)