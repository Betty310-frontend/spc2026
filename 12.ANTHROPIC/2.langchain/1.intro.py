from dotenv import load_dotenv

# from langchain_openai import ChatOpenAI

# pip install langchain-anthropic
from langchain_anthropic import ChatAnthropic

load_dotenv()

llm = ChatAnthropic(model='claude-sonnet-4-6')

# response = llm.invoke('인공지능에 대해서 설명해줘.')
response = llm.invoke('이번 주 날씨 어때?')
print(response.content)