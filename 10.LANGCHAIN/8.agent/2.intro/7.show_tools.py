from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.load_tools import get_all_tool_names

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini')

print('-' * 20, '사용 가능한 도구 목록', '-' * 20)
names = sorted(get_all_tool_names())

for name in names:
    print(f" - {name}")

print(f"\n총 {len(names)}개의 도구가 있습니다.")

"""
HITL - Human in the loop
"""