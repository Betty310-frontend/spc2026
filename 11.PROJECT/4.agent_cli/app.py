"""
금융 도우미 에이전트 챗봇 만들기

- langchain 관련 라이브러리 불러오기

- 툴 추가
  - from fin_tools.py
"""
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from fin_tools import TOOLS

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini')

SYSTEM = """
    당신은 금융 정보 비서입니다.
    다음과 같은 도구들을 활용해서 사용자의 질문에 답변하세요.
    
    도구 사용 가이드:
    1. get_news
      - 네이버 뉴스를 가져오는 도구입니다. 'query' 인자로 검색어를 입력하면 관련 뉴스를 반환합니다.
    2. get_company_info
      - 구글 검색으로 기업 개요/최근 정보를 조회하는 도구입니다. 'company_name' 인자로 기업명을 입력하면 관련 정보를 반환합니다.
    3. get_exchange_rate
      - 환율을 조회하는 도구입니다. 'rate_code'에 인자로 통화 코드를 입력하면 원화(KRW) 기준으로 환율을 반환합니다.
    4. get_stock_price
      - 주가를 조회하는 도구입니다. 'ticker' 인자로 기업의 티커 코드를 입력하면 주가를 반환합니다.

    환율/주가 같은 수치 데이터는 반드시 도구를 통해서 확인하세요. (추측 또는 과거 데이터 이용 금지)
    출처 링크가 있으면 반드시 함께 제시하세요.
"""

agent = create_agent(llm, TOOLS, system_prompt=SYSTEM)

def ask(question):
    # agent를 통해 해당 질문을 호출한다.
    try:
        result = agent.invoke({
            "messages": [("user", question)]
        })
        tool_used = [call["name"] for msg in result["messages"]
                if getattr(msg, "tool_calls", None) for call in msg.tool_calls]
        print(f"사용된 도구: {tool_used or '(없음)'}")
        return result['messages'][-1].content
    except Exception as e:
        return f"오류가 발생했습니다: {str(e)}"

if __name__ == '__main__':
    print('=== 데모 명령어 실행 ===')
    for question in ['삼성전자 주가 알려줘', '달러 환율 얼마야?', '엔비디아 관련 최근 뉴스 뭐 있어?']:
        response = ask(question)
        print(f"질문: {question}")
        print(f"응답: {response}\n")

    print('=== 수동 질의 응답 시작 ===')
    while True:
        # 사용자로부터 질문을 받아서 'q', 'quit', 'exit' 가 올 때 종료
        user_input = input("질문을 입력하세요 (종료하려면 'q', 'quit', 'exit' 입력): ")
        question = user_input.strip().lower()
        if question in ['q', 'quit', 'exit']:
            print("프로그램을 종료합니다.")
            break
        response = ask(question)
        print(f"응답: {response}\n")