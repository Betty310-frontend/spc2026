from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini')

def make_chain(system_message):
    prompt = ChatPromptTemplate.from_messages([
        ('system', system_message),
        ('user', '{question}')
    ])
    return prompt | llm | StrOutputParser()

# 개발자 / 요리사 / 일반 사용자 유형을 분기하는 체인
developer_chain = make_chain("당신은 파이썬 개발자입니다.")
chef_chain = make_chain("당신은 요리사입니다.")
general_chain = make_chain("당신은 일반 어시스턴트입니다.")

branch = RunnableBranch(
    (lambda x: "파이썬" in x["question"] or "코드" in x["question"], developer_chain),
    (lambda x: "요리" in x['question'] or "레시피" in x['question'], chef_chain),
    general_chain
)

questions = [
    "파이썬 리스트 정렬 코드 알려줘.",
    "김치찌개 레시피 알려줘.",
    "오늘 날씨 어때?"
]

for question in questions:
    result = branch.invoke({'question': question})
    print(f"질문: {question}\n답변: {result}\n{'-'*50}")