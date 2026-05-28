"""
목적
- 필요한 비즈니스 로직에 맞는 SQL 구문을 작성해준다.
"""


from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
)
from langchain_core.runnables import RunnableLambda

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 SQL 전문가입니다. 다음 질문에 맞는 SQL 구문을 작성해주세요. SQL 쿼리문만 답변하고 설명은 하지 마세요."),
    ("user", "DB Schema: \n{schema}\n\nUser Query: \n{query}"),
])

schema = """
Table: users
- id (integer, primary key)
- name (string)
- email (string)
- signup_date (date)

Table: orders
- id (integer, primary key)
- user_id (integer, foreign key to users.id)
- product_name (string)
- price (decimal)
- created_at (datetime)
"""

chain = chat_prompt | llm | RunnableLambda(lambda x: {'sql': x.content.strip()})

questions = [
    "2023년 1월 1일 이후 가입한 사용자의 이름과 이메일을 조회해줘.",
    "주문 금액이 50,000원 이상인 주문 목록을 조회해줘.",
    "사용자별 총 주문 금액을 계산해줘.",
    "가장 최근에 주문한 사람과 그 상품명을 5개 보여줘.",
    "회원 가입 후 한번도 주문하지 않은 사람 이름을 알려줘."
]

for idx, question in enumerate(questions):
    print(f"{'-'*10} 질문 {idx+1} {'-'*10}")
    result = chain.invoke({'schema': schema, 'query': question})
    print(result['sql'])