import os
from dotenv import load_dotenv

from langchain_openai import OpenAI # 단발성 질문 (Instruct Model)
from langchain_openai import ChatOpenAI # 대화형 질문 (Chat Model) - 대화의 맥락을 이해하고 유지하는 능력이 뛰어남. 일반적으로 더 자연스러운 답변을 생성할 수 있음.

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

llm = OpenAI(api_key=openai_api_key, model="gpt-3.5-turbo-instruct") # 단발성 질문에 적합한 모델

prompt = '다음 문장을 한국말로 번역해줘. Good Morning!'
result = llm.invoke(prompt)
print(result)

llm2 = ChatOpenAI(api_key=openai_api_key, model="gpt-4o-mini", temperature=0.9) # temperature: 답변의 창의성 정도를 조절하는 매개변수. 낮은 값은 더 결정적이고 일관된 답변을 생성하는 반면, 높은 값은 더 다양하고 창의적인 답변을 생성함.
prompt2 = '게임 회사를 창업하려고 하는데, 이름 후보군 3개 지어줘.'
print(llm2.invoke(prompt2))

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
prompt3 = [
    SystemMessage(content='당신은 창의력이 높은 작명가입니다.'),
    HumanMessage(content='게임 회사를 창업하려고 해. 이름 후보군 3개 지어줘.'),
]

print(llm2.invoke(prompt3))