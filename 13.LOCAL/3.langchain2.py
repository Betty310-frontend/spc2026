from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(model='mistral')

prompt = PromptTemplate.from_template(
    """
    다음 주제로 작성할만한 블로그 글의 개요 5가지 만들어줘.
    답변은 반드시 한국말로 해줘.
    ---\n\n
    주제: {topic}                                      
    """
)

chain = prompt | llm | StrOutputParser()

response = chain.invoke({"topic": "로컬 LLM 모델의 활용"})

print(response)