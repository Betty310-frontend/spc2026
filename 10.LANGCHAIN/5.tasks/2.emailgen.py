"""
목적
- 다양한 목적에 맞는 이메일을 생성하는 체인을 만들어봅시다.
"""


from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini', max_tokens=1000)

chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "당신은 기업의 커뮤니케이션 전문가입니다."
        "포멀하게 전문가 톤으로 이메일을 작성해주세요."
    ),
    HumanMessagePromptTemplate.from_template(
        "수신자 '{recipient}'에게 다음 주제 '{topic}'에 대한 미팅 요청을 하는 메일을 작성해주세요."
    ),
])

chain = chat_prompt | llm | StrOutputParser()

# 다양한 수신자, 다양한 주제로 이메일을 생성해봅시다.
recipients = ["마케팅 팀", "개발 팀", "영업 팀", "인사 팀"]
topics = [
    "신제품 출시 전략", 
    "분기별 개발 성과 지표", 
    "개인별 매출 목표치 달성 현황", 
    "개발을 잘 못해서 맨날 버그만 발생시키는 개발자 해고"
]

for recipient, topic in zip(recipients, topics):
    result = chain.invoke({
        'recipient': recipient,
        'topic': topic
    })
    print(f"{'-'*10} 생성된 이메일 {'-'*10}")
    print(f"수신자: {recipient}")
    print(f"주제: {topic}")
    print(result)