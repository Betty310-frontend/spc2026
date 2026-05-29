from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini')

parser = StrOutputParser()
prompt = ChatPromptTemplate.from_messages([
    ('system', '당신은 친절한 챗봇입니다.'), 
    MessagesPlaceholder('history'),
    ('user', '{input}'),
])

chain = prompt | llm | parser

history = InMemoryChatMessageHistory()

def chat(message):
    print(f"질문: {message}")
    answer = chain.invoke({
        'input': message,
        # 'history': history.messages # 우리의 저장소에 있는 메시지 그래도 다 저장
        'history': history.messages[-10:] # 최근 10개의 메시지만 저장 (메모리 제한)  
    })
    print(f"답변: {answer}")
    history.add_user_message(message) # 사용자의 메시지 저장
    history.add_ai_message(answer) # 챗봇의 답변 저장

chat("안녕하세요.")
chat("제 이름은 홍길동입니다.")
chat("저는 겨울에 바닷가에 가서 서핑하는 것을 좋아합니다.")
chat("제 이름과 취미를 뭐였죠?")