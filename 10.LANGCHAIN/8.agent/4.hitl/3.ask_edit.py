from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AIMessage

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

question = "bob에게 1만원을 송금해."

print(f"[유저] {question}\n")

result = agent.invoke({
    "messages": [("user", question)]
}, config=config)

print("="*30)
print(result)
print("="*30)

# 현재 멈춰 있는 상태 조회
ai_msg = agent.get_state(config).values['messages'][-1]
call = ai_msg.tool_calls[0]

print(f"[에이전트 제안] {call['name']} ({call['args']})\n\n")

# 2. 해당 상태를 사용자가 수동으로 수정
edited = {**call, "args": {**call['args'], 'amount': 5000}}
fixed = AIMessage(content=ai_msg.content, tool_calls=[edited], id=ai_msg.id)
agent.update_state(config, {"messages":[fixed]})
print(f"  -> 사람이 수정 10000 -> 5000\n\n")

# 3. 이어서 실행
result = agent.invoke(None, config=config)
print(f"[최종] {result}")
