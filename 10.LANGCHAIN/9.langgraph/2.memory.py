import uuid

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini')

graph = StateGraph(MessagesState)

memory = MemorySaver()

def call_model(state):
    """
    LLM 메시지를 전달하고 응답하는 함수
    """
    messages = state['messages']
    system_message = SystemMessage(content="당신은 친절한 AI비서입니다.")
    all_messages = [system_message] + messages

    print("모델 호출 함수 실행 중... 메시지 수:", len(all_messages))
    response = llm.invoke(all_messages)
    print(f"모델 응답 생성 완료: {response.content[:50]}...")
    return {"messages": response}

graph.add_node("model", call_model)
graph.add_edge(START, "model")
graph.add_edge("model", END)

app = graph.compile(checkpointer=memory)

thread_id1 = str(uuid.uuid4())
config1 = {"configurable": {"thread_id": thread_id1}}

# 대화가 이어지는지 확인
first_input = "안녕하세요. 제 이름은 김철수입니다."
result1 = app.invoke({"messages": [HumanMessage(content=first_input)]}, config=config1)
second_input = "제 이름이 뭐라구요?"
result2 = app.invoke({"messages": [HumanMessage(content=second_input)]}, config=config1)

print("-" * 50)
print(f"AI 응답: {result2['messages'][-1].content}")

thread_id2 = str(uuid.uuid4())
config2 = {"configurable": {"thread_id": thread_id2}}

first_input = "안녕하세요. 제 이름은 홍길동입니다."
result3 = app.invoke({"messages": [HumanMessage(content=first_input)]}, config=config2)
second_input = "제 이름이 뭐라구요?"
result4 = app.invoke({"messages": [HumanMessage(content=second_input)]}, config=config2)

first_input = "저의 직업은 프로그래머입니다."
result3 = app.invoke({"messages": [HumanMessage(content=first_input)]}, config=config1)
second_input = "제 이름이 무엇이고, 저는 무슨 일을 하나요?"
result4 = app.invoke({"messages": [HumanMessage(content=second_input)]}, config=config1)

print("-" * 50)
print(f"AI 응답: {result2['messages'][-1].content}")

second_input = "제 이름이 무엇이고, 저는 무슨 일을 하나요?"
result4 = app.invoke({"messages": [HumanMessage(content=second_input)]}, config=config2)

print("-" * 50)
print(f"AI 응답: {result2['messages'][-1].content}")