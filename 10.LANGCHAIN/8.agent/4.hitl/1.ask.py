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

agent = create_agent(
    llm, tools=[send_payment], 
    checkpointer=checkpoint, 
    interrupt_before=['tools']
)

config = {
    "configurable": {
        "thread_id": "t001"
    }
}

question = "홍길동에게 10000원 송금해줘."

print(f"[유저] {question}\n")

result = agent.invoke({
    "messages": [("user", question)]
}, config=config)

call = result['messages'][-1].tool_calls[0] # 정지 시점 (도구를 부르기 직전)

print(f"[일시정지] {call['name']} ({call['args']})\n\n")

human_result = input('이대로 실행할까요? (y/n)').strip().lower()
if human_result == 'y':
    result = agent.invoke(None, config=config) # 이어서 실행
    print(f"[최종 결과] {result['messages'][-1].content}\n\n")
else:
    print("[중단] 사용자 요청에 의해 실행이 취소되었습니다.\n\n")