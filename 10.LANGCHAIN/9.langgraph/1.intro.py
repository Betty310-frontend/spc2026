from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from langgraph.graph import StateGraph, START, END, MessagesState

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini')

# MessageState는 기본 타입 - 여기 MessageState에는 SystemMessage/AIMessage/HumanMessage가 포함될 수 있다.
graph = StateGraph(state_schema=MessagesState)

def call_model(state):
    """
    LLM 메시지를 전달하고 응답하는 함수
    """
    messages = state['messages']
    system_message = SystemMessage(content="당신은 친절한 AI비서입니다.")
    all_messages = [system_message] + messages

    print("모델 호출 함수 실행 중... 메시지 수:", len(all_messages))
    response = llm.invoke(all_messages)
    print("모델 응답 생성 완료: ", response.content[:50])
    return {"messages": response}

graph.add_node("model", call_model)
graph.add_edge(START, "model")
graph.add_edge("model", END)

app = graph.compile()

user_input = input("\n질문을 입력하세요: ")
result = app.invoke({"messages": [HumanMessage(content=user_input)]})

for i, message in enumerate(result['messages'], start=1):
    print(f"메시지 {i}: {message.type} - {message.content}")