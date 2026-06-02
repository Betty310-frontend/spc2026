from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_tavily import TavilySearch

load_dotenv()

# 구글 검색은 원래 구글 API 키를 사용해야 하지만, 이번 예시에서는 웹 검색 도구로 대체해서 사용해봅시다.
# 쉽게 만들어주는 사이트가 있음. Serf, Serper, Tavily 등등

# pip install langchain-tavily

web_search = TavilySearch(max_results=3)
llm = ChatOpenAI(model='gpt-4o-mini')
agent = create_agent(llm, [web_search])

result = agent.invoke({
    "messages": [
        ('user', 'LangChain의 최신 버전은?')
    ]
})

print(result['messages'][-1].content)

