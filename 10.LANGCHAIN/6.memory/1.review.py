from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
)

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini')

parser = StrOutputParser()
prompt = ChatPromptTemplate.from_messages([
    ('system', "당신은 친절한 챗봇입니다."), # 가상의 인물 설정. 페르소나
    ('user', "{input}"), # 사용자의 질문
    # ('ai', "위 텍스트에 대한 리뷰를 제공해주세요. 구체적이고 건설적인 피드백을 제공해주세요.") # 챗봇 답변
])

chain = prompt | llm | parser

print(chain.invoke({'input': '안녕하세요, 나는 홍길동입니다.'}))
print(chain.invoke({'input': '그래서 내가 누구라고?'}))

print('-' * 50)

prompt_with_history = ChatPromptTemplate.from_messages([
    ('system', "당신은 친절한 챗봇입니다."), # 가상의 인물 설정. 페르소나
    MessagesPlaceholder('history'), # 여기 공간에 우리의 대화 내용을 넣으려고 함
    ('user', "{input}"), # 사용자의 질문
])

chain2 = prompt_with_history | llm | parser

history_example = [
    HumanMessage(content="안녕하세요, 나는 홍길동입니다."),
    AIMessage(content="안녕하세요 홍길동님! 만나서 반갑습니다. 어떻게 도와드릴까요?"),
]

answer = chain2.invoke({
    'history': history_example, 
    'input': '그래서 내가 누구라고?'
})
print(answer)