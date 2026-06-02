import json
from typing import Literal
from pydantic import BaseModel, Field

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

class SendEmailInput(BaseModel):
    """
    이메일 전송 도구의 인자
    """
    to: str = Field(description="수신자 이메일 주소 (반드시 유효한 이메일 형식이어야 함)")
    subject: str = Field(description="이메일 제목 (50자 이내, 간결하게)")
    body: str = Field(description="이메일 본문 내용 (반드시 한국어로 작성)")
    priority: Literal['low', 'normal', 'high'] = Field(default="normal", description="이메일 우선순위, urgent한 경우 'high' 사용")

@tool(args_schema=SendEmailInput)
def send_email(to: str, subject: str, body: str, priority: str='normal') -> str:
    """
    사용자가 요청할 때 이메일을 보낸다.
    (실제로는 보내지 않고 보낼 결과만 출력함.)
    """
    print(f"[가짜 전송] to={to}, priority={priority}")
    print(f"제목: {subject}")
    print(f"본문: {body}")
    return f"이메일이 {to}에게 전송되었습니다. (priority={priority})"

class SearchInput(BaseModel):
    """
    검색 도구의 인자
    """
    query: str = Field(description="검색어")
    max_results: int = Field(default=5, ge=1, le=20, description="결과 갯수 (1~20 사이)")
    sort_by: Literal['relevance', 'date'] = Field(
        default='relevance',
        description="정렬 기준. 최신 정보가 중요하면 date 사용, 일반적인 검색은 relevance 사용"
    )

@tool(args_schema=SearchInput)
def search(query: str, max_results: int=5, sort_by: str='relevance') -> list[str]:
    """
    주어진 쿼리로 검색을 수행한다.
    """
    return [f'결과 {i+1} {query} (정렬={sort_by})' for i in range(max_results)]

tools = [send_email, search]
llm = ChatOpenAI(model='gpt-4o-mini')

llm_with_tools = llm.bind_tools(tools)

print("--- 툴 명세 확인 ---\n")
print(json.dumps(send_email.args_schema.model_json_schema(), indent=2, ensure_ascii=False))
print("\n")
print(json.dumps(search.args_schema.model_json_schema(), indent=2, ensure_ascii=False))

print("\n--- 툴 테스트 ---\n")

questions = [
    "alice@example.com에게 회의 일정 변경이라는 제목으로 메일 보내줘. 본문은 '회의가 내일 3시로 변경되었습니다.'로 보내고, 긴급해.",
    "파이썬 비동기 프로그래밍 최신 자료 10개만 날짜순으로 검색해줘.",
    "오늘 점심 메뉴로 샌드위치와 콜라를 주문해줘."
]

SYSTEM = (
    "도구는 적합할 때만 사용하세요. 그리고 입력 인자들을 잘 확인하고, 오류가 없도록 호출하시오."
    "호출이후 오류가 발생한 경우 도구의 목적와 인자값을 잘 확인하고 재시도 하시오"
    "그러나 재시도는 최대 2회만 하시오"
    "적합한 도구를 발견하지 못했을 경우, '해당 작업을 수행할 수 있는 도구가 없습니다.'라고 답변하시오."
)

for q in questions:
    print(f"\n질문: {q}")
    r = llm_with_tools.invoke([
        SystemMessage(SYSTEM),
        HumanMessage(q)
    ])

    # print(f"{'-'*50} {r} {'-'*50}\n\n")

    if not r.tool_calls:
        print(f" (도구 없을 때): {r.content}")
    else:
        for call in r.tool_calls:
            print(f" -> {call['name']} ({call['args']})")

            # 실제 툴 함수 호출
            try:
                name2tool = {t.name: t for t in tools}
                result = name2tool[call['name']].invoke(call['args'])
                print(f"    결과: {result}")
            except Exception as e:
                print(f"    오류 발생: {e}")