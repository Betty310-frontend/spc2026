from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini')

checkpoint = MemorySaver()

@tool
def send_payment(recipient: str, amount: int) -> str:
    """
    수신자에게 지정 금액을 송금한다.
    """
    return f"{recipient}에게 {amount}원 송금 완료"

@tool
def get_balance(account_id: str) -> int:
    """
    계좌의 잔액을 조회한다.
    """
    return {"alice": 1_000_000, "bob": 500_000}.get(account_id, 0)

tools = [send_payment, get_balance]

agent = create_agent(
    llm, tools=tools, 
    checkpointer=checkpoint, 
    interrupt_before=['tools']
)

config = {
    "configurable": {
        "thread_id": "t001"
    }
}

question = "alice의 잔액에서 bob에게 10,000원 송금해줘."

print(f"[유저] {question}\n")

result = agent.invoke({
    "messages": [("user", question)]
}, config=config)

# 하나의 질문에서 여러 개의 도구를 호출하는 경우
while result['messages'][-1].tool_calls:
    last_msg = result['messages'][-1]

    for call in last_msg.tool_calls:
        print(f"[일시정지] {call['name']} ({call['args']})\n\n")

    if last_msg.tool_calls[0]['name'] != 'send_payment':
        # 송금이 아닌 다른 도구가 호출된 경우 (예: 잔액 조회)에는 바로 이어서 실행
        result = agent.invoke(None, config=config) # 이어서 실행
        continue

    human_result = input('이대로 실행할까요? (Y/N)  ').strip().lower()
    if human_result == 'y':
        result = agent.invoke(None, config=config) # 이어서 실행
        print(f"[최종 결과] {result['messages'][-1].content}\n\n")
    else:
        print("[중단] 사용자 요청에 의해 실행이 취소되었습니다.\n\n")
        break