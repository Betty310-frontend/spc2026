# pip install langchain langchain-openai

import os
from dotenv import load_dotenv

# from langchain.llm import OpenAI # 구버전
from langchain_openai import OpenAI

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

llm = OpenAI(api_key=openai_api_key, model="gpt-4o-mini")
# print(llm)

prompt = '오늘 저녁은 무엇을 먹을까요?'
result = llm.invoke(prompt)
print(result)