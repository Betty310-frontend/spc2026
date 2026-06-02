from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

load_dotenv()

@tool
def get_word_length(word:str) -> int:
    """
    단어의 길이를 반환한다.
    ex) apple -> 5
    """
    return len(word)

@tool
def calculate_tip(amount:float, percent:float) -> float:
    """
    음식점 영수증 금액과 팁 비율(%)을 입력받아서 팁 금액을 계산한다.
    ex) amount=100, percent=15 -> 15.0
    """
    return amount * (percent / 100)

@tool
def search_user(user_id: str) -> dict:
    """
    사용자 ID를 입력받아서 사용자 정보를 반환한다.
    존재하지 않으면 빈 딕셔너리({})를 반환한다.
    ex) user_id="user123" -> {"name": "Alice", "age": 30}
    """

    db = {
        "u001": {"name":"홍길동", "city":"서울", "age": 25},
        "u002": {"name":"김철수", "city":"부산", "age": 28},
        "u003": {"name":"이영희", "city":"대구", "age": 22},
    }
    
    return db.get(user_id, {})

tools = [get_word_length, calculate_tip, search_user]
llm = ChatOpenAI(model='gpt-4o-mini')
llm_with_tools = llm.bind_tools(tools)

print("--- 툴 상태 확인 ---\n")
for tool in tools:
    print(f"\n툴 이름: {tool.name}, 설명: {tool.description}")
    print(f"인자 스키마: {tool.args_schema.model_json_schema()}")

print("\n--- 툴 테스트 ---\n")
questions = [
    "this-is-a-long-sentence 문장에 글자는 몇 개야?",
    "5만원 영수증에 15% 팁을 주려면?",
    "홍길동 사용자 정보를 알려줘.",
    "u001 사용자 정보는?"
]

name2tool = {t.name: t for t in tools}

for question in questions:
    r = llm_with_tools.invoke(question)
    print(f"\n질문: {question}")
    for call in r.tool_calls:
        print(f" -> {call['name']} ({call['args']})")

        result = name2tool[call['name']].invoke(call['args']) # 실제 툴 함수 호출
        print(f"    결과: {result}")