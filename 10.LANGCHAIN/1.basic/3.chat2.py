from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()

openai_model = 'gpt-4o-mini'

llm = ChatOpenAI(model=openai_model)

prompt = [
    SystemMessage(content='당신은 경력 10년 차 호텔 쉐프입니다.'),
    HumanMessage(content='오늘 저녁 메뉴를 추천해줘.'),
    AIMessage(content='비빔밥은 어떠신가요?'),
    HumanMessage(content='좋아. 그걸 만들기 위한 재료는?'),
]

result2 = llm.invoke(prompt)
print(result2.content)