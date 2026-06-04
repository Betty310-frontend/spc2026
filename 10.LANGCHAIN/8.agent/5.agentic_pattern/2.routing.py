from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini')
parser = StrOutputParser()

technical_prompt = ChatPromptTemplate.from_template(
    """
    당신은 기술 지원 전문가 입니다. 단계별로 정확한 문제 해결 방법을 안내해주세요.

    고객문의: {question}
    ---
    답변은 다음 형식을 따르세요:
    [기술 지원 답변]
    """
)
technical_chain = technical_prompt | llm | parser

billing_prompt = ChatPromptTemplate.from_template(
    # ex) 고객이 환불 또는 회원탈퇴를 원할 경우, 정중하게 사과를 하고 다른 상품 구매를 유도해주세요.
    """
    당신은 결제 및 구독 전문 상담원 입니다. 사내 정책에 따라 안내하고, 친절하게 응대해주세요.

    고객문의: {question}
    ---
    답변은 다음 형식을 따르세요:
    [결제 지원 답변]
    """
)
billing_chain = billing_prompt | llm | parser

general_prompt = ChatPromptTemplate.from_template(
    """
    당신은 친절한 고객 지원 전문가 입니다. 고객의 질문에 친절하게 답변해주세요.

    고객문의: {question}
    ---
    답변은 다음 형식을 따르세요:
    [고객 지원 답변]
    """
)
general_chain = general_prompt | llm | parser

route_map = {
    'technical': technical_chain, # 기술적인 질문에 답변하는 체인
    'billing': billing_chain,     # 결제 관련 질문에 답변하는 체인
    'general': general_chain      # 그외 기타, 일반적인 질문에 답변하는 체인
}

classifier_prompt = ChatPromptTemplate.from_template(
    """
    다음 고객 문의가 기술적인 질문인지, 결제 관련 질문인지, 일반적인 질문인지 분류해주세요. 
    기술적인 질문이면 'technical', 결제 관련 질문이면 'billing', 그 외에는 'general'로 답해주세요.

    고객문의: {question}
    ---
    분류 결과:
    technical, billing, general 중 하나로 답해주세요.
    """
)
classifier_chain = classifier_prompt | llm | parser

# 사용자의 질문을 받아 적절한 챗봇으로 라우팅한다.
def route_query(input: dict) -> str:
    query = input['question'].lower()

    # 1단계. 분류를 시켜서 카테고리를 가져온다.
    category = classifier_chain.invoke({'question': query}).strip().lower()
    # print(f"분류 결과: {category}")

    # 2단계. 해당 카테고리 체인을 다시 호출한다.
    chain = route_map.get(category, general_chain)
    response = chain.invoke({'question': query})

    return f"[{category.upper()}] {response}"

routing_chain = RunnableLambda(route_query)

if __name__ == "__main__":
    print("=== Testing Routing Chain ===")
    test_questions = [
        "프로그램이 자꾸 충돌하는데 어떻게 해야 하나요?",
        "구독을 취소하고 환불받고 싶어요.",
        "이 서비스에서는 어떤 기능을 제공하나요?",
        "API 연동 시 인증 오류가 발생합니다.",
        "I can't log in to my account after the recent update.",
    ]

    for i, question in enumerate(test_questions, 1):
        print(f"\n{'-' * 60}")
        print(f"[질문 {i}] {question}")
        result = routing_chain.invoke({"question": question})
        print(f"[응답 {i}] {result}")