from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini')

# 우리의 도구를 정의할 때 @tool 데코레이터 사용, 함수 내에 주석을 쓰면, 그 내용을 읽어서 에이전트가 어떻게 사용할지 파악함
@tool
def calculator(expression):
    """
    수학식을 계산한다.
    예시: 53 * 7 + 2
    """
    return str(eval(expression))

agent = create_agent(llm, [calculator]) # calculator는 위에서 정의한 나의 에이전트입니다.

# result = agent.invoke({'messages': [('user', '(50 * 7 + 2) / 5는 얼마야?')]})
result = agent.invoke({'messages': [('user', '복잡한 수식을 계산해줘. 50에서 5를 곱하고, 3을 나눈 다음, 2를 빼고 마지막으로 5로 나눠줘.')]})

print('=== 전체 메시지 흐름 ===')
for msg in result['messages']:
    if hasattr(msg, 'tool_calls') and msg.tool_calls:
        for call in msg.tool_calls:
            print(f"도구 호출: {call['name']}({call['args']})")
    if msg.content:
        prefix = {"human": "[사용자]", "ai": "[AI]", "tool": "[도구 결과]"}.get(msg.type, "[알 수 없는 역할]")
        print(f"{prefix} {msg.content}")
# print(result)
