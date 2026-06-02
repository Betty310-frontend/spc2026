from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent

load_dotenv()

@tool
def calculator(expression: str) -> str:
    """
    수학 식을 계산한다.
    ex) 53 * 7 + 2
    """
    try:
        """
        예외처리를 하지 않으면 LLM이 맘대로 입력하는 값으로 우리 코드가 죽을 수 있음.
        """
        return str(eval(expression, {"__builtins__": {}}, {})) # 내부 빌트인 함수들의 호출을 금지
    except Exception as e:
        return f"계산오류: {e}"    
    
llm = ChatOpenAI(model='gpt-4o-mini')
agent = create_agent(llm, tools=[calculator])

result = agent.invoke({
    # 'messages': [("user", "10 나누기 2 곱하기 5는?")]
})

print(f"최종 답변: {result['messages'][-1].content}")