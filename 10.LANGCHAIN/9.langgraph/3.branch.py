import uuid

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.runnables import RunnableConfig

from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.memory import MemorySaver

from typing import TypedDict, List, Dict, Any

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini')

def get_weather():
    return "오늘 서울의 날씨는 맑고, 기온이 22도 입니다."

def get_news():
    return "최신 뉴스: 오늘 삼성전자 주가는 -9% 하락 중입니다."

class State(TypedDict):
    messages: List[AIMessage]
    topic: str

graph = StateGraph(State)
memory = MemorySaver()

def topic_router(state: State, config: RunnableConfig) -> str:
    """
    사용자 질문에 따라서 경로를 라우팅하는 함수
    """
    last_message = state['messages'][-1].content.lower() # News, news, NEWS...
    if "날씨" in last_message:
        print("라우터: '날씨'를 감지하여 weather 라우팅으로 보내는 중...")
        return 'weather'
    if "뉴스" in last_message:
        print("라우터: '뉴스'를 감지하여 news 라우팅으로 보내는 중...")
        return 'news'
    print("라우터: 일반 대화 감지 -> chat 노드로 라우팅하는 중...")
    return 'chat'
    
def router_node(state: State, config: RunnableConfig) -> Dict[str, Any]:
    # 특별히 할 일 없음. 그냥 placeholder 역할
    return {}

def weather_node(state: State, config: RunnableConfig) -> Dict[str, Any]:
    weather_info = get_weather()
    response = llm.invoke([
        SystemMessage(content="당신은 날씨 전문가입니다."),
        HumanMessage(content=f"다음 날씨 정보를 사용자에게 친절하게 설명해주세요: {weather_info}")
    ])

    return {"messages": state["messages"] + [response], "topic": "weather"}

def news_node(state: State, config: RunnableConfig) -> Dict[str, Any]:
    news_info = get_news()
    response = llm.invoke([
        SystemMessage(content="당신은 뉴스 전문가입니다."),
        HumanMessage(content=f"다음 뉴스 정보를 사용자에게 친절하게 설명해주세요: {news_info}")
    ])
    return {"messages": state["messages"] + [response], "topic": "news"}

def chat_node(state: State, config: RunnableConfig) -> Dict[str, Any]:
    messages = state['messages']

    response = llm.invoke([
        SystemMessage(content="당신은 친절한 AI비서입니다."),
        HumanMessage(content=f"{messages}")
    ])
    return {"messages": state["messages"] + [response], "topic": "chat"}

graph.add_node("router", router_node)
graph.add_node("weather", weather_node)
graph.add_node("news", news_node)
graph.add_node("chat", chat_node)

graph.add_edge(START, "router")
graph.add_conditional_edges(
    "router", 
    topic_router, 
    path_map={
        "weather": "weather",
        "news": "news",
        "chat": "chat"
    }
)
graph.add_edge("weather", END)
graph.add_edge("news", END)
graph.add_edge("chat", END)

app = graph.compile(checkpointer=memory)
thread_id = str(uuid.uuid4())
config = {"configurable": {"thread_id": thread_id}}

while True:
    user_input = input("\n질문을 입력하세요: ")
    if user_input.lower() in ["종료", "exit", "quit", "q"]:
        break
    result = app.invoke({"messages": [HumanMessage(content=user_input)], "topic": ""}, config=config)
    
    print(f"AI 토픽: {result['topic']}\n응답: {result['messages'][-1].content}")
