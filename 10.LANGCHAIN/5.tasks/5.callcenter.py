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

shipping_prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 친절한 배송 상담원입니다. 핵심만 간단히 안내하세요."),
    (
        "user",
        "다음 고객 문의에 대해 배송 조회/배송 관련 상담으로 답변하세요.\n"
        "- 주문번호가 없으면 확인 방법을 안내하세요.\n"
        "- 답변은 3문장 이내로 작성하세요.\n\n"
        "문의: {question}",
    ),
])

payment_prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 결제 상담원입니다. 결제/환불/영수증 이슈를 정확히 안내하세요."),
    (
        "user",
        "다음 고객 문의에 대해 결제 관련 상담으로 답변하세요.\n"
        "- 결제 실패, 환불, 영수증 재발급 관점에서 안내하세요.\n"
        "- 답변은 3문장 이내로 작성하세요.\n\n"
        "문의: {question}",
    ),
])

tech_prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 기술지원 상담원입니다. 문제 원인과 해결 단계를 간단히 제시하세요."),
    (
        "user",
        "다음 고객 문의에 대해 기술지원 상담으로 답변하세요.\n"
        "- 앱/웹 오류, 로그인, 실행 문제를 우선적으로 다루세요.\n"
        "- 답변은 3문장 이내로 작성하세요.\n\n"
        "문의: {question}",
    ),
])

shipping_chain = shipping_prompt | llm | parser
payment_chain = payment_prompt | llm | parser
tech_chain = tech_prompt | llm | parser


def is_shipping_question(x: dict) -> bool:
    q = x["question"]
    keywords = ["배송", "출고", "택배", "운송장", "도착", "배송조회", "언제 와"]
    return any(k in q for k in keywords)


def is_payment_question(x: dict) -> bool:
    q = x["question"]
    keywords = ["결제", "환불", "카드", "취소", "영수증", "청구", "입금"]
    return any(k in q for k in keywords)


callcenter_branch = RunnableBranch(
    (is_shipping_question, shipping_chain),
    (is_payment_question, payment_chain),
    tech_chain,
)


if __name__ == "__main__":
    questions = [
        {"question": "주문한 상품 배송조회 어떻게 하나요?"},
        {"question": "결제는 됐는데 주문이 안 됐어요. 환불 가능한가요?"},
        {"question": "앱 로그인 버튼을 눌러도 화면이 멈춰요."},
    ]

    for item in questions:
        print(f"{'-'*10} [고객 문의] {'-'*10}\n")
        print(f"{item['question']}\n")
        answer = callcenter_branch.invoke(item)
        print(f"{'-'*10} [상담 답변] {'-'*10}\n")
        print(f"{answer}\n")