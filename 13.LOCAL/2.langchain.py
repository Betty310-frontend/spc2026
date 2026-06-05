# pip install langchain-ollama
from langchain_ollama import ChatOllama

llm = ChatOllama(model='mistral')

response = llm.invoke("안녕? 너를 한 마디로 소개해줘.")

print(response.content)
