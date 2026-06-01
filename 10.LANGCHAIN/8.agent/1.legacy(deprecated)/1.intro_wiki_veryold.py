"""
에이전트를 통해서, 본연의 LLM 즉, 대화의 기능 외적인 기능을 쓸 수 있음.

pip install wikipedia
"""

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import initialize_agent, AgentType

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.3)

tools = load_tools(['wikipedia'])

# 에이전트 초기화
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True # 나중에는 False, 에이전트의 생각과 행동을 볼 수 있음
)

result = agent.invoke({"input": "인공지능의 역사에 대해 알려줘."})
print(result['output'])