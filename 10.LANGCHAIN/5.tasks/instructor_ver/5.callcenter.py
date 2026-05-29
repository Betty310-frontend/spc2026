"""
목적
- 질문 유형에 따라 적합한 항목으로 답변한다.
- 질문 입력 -> 배송조회 및 상담
          -> 결제관련 상담 
          -> 기술지원 상담
- RunnableBranch를 활용하여 질문 유형에 따라 적합한 항목으로 분기 수행
"""

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableBranch

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini')
parser = StrOutputParser()

def make_chain(role):
    prompt = ChatPromptTemplate.from_messages([
                ('system', role),
                ('user', "{question}")
            ])
    
    return prompt | llm | parser

payment_chain = make_chain("당신은 결제 관련 상담 전문가입니다. 고객의 결제 관련 질문에 친절하게 답변해주세요.")
delivery_chain = make_chain("당신은 배송 조회 및 상담 전문가입니다. 고객의 배송 관련 질문에 친절하게 답변해주세요.")
tech_support_chain = make_chain("당신은 기술 지원 상담 전문가입니다. 고객의 기술 지원 관련 질문에 친절하게 답변해주세요.")
general_chain = make_chain("당신은 고객 상담 전문가입니다. 고객의 일반적인 질문에 친절하게 답변해주세요.")

branch = RunnableBranch(
    (lambda x: any(k in x['question'] for k in ['결제', '지불', '환불', '청구']), payment_chain),
    (lambda x: any(k in x['question'] for k in ['배송', '배달', '택배', '도착', '반품']), delivery_chain),
    (lambda x: any(k in x['question'] for k in ['기술', '지원', '문제', '오류', '안돼요', '에러']), tech_support_chain),
    general_chain # 모든 조건에 해당하지 않는 질문은 일반 상담으로 처리
)

questions = [
    "배송이 아직 안 왔어요. 언제 도착하나요?",
    "결제는 어떻게 하나요? 카드로 할 수 있나요?",
    "앱이 자꾸 오류가 나요. 로그인이 안돼요.",
    "이용 시간은 어떻게 되나요?"
]


for q in questions:
    print('-' * 50)
    result = branch.invoke({'question': q})
    print(f"[고객문의] {q}")
    print(f"[답변] {result}")