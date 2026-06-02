import sqlite3

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini')

# 메모리 내 임시 데이터베이스 생성, check_same_thread=False는 여러 스레드에서 접근 가능하도록 설정
conn = sqlite3.connect(':memory:', check_same_thread=False) 
conn.executescript(
    """
    CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, city TEXT, age INTEGER);      
    CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price INTEGER, category TEXT);      
    CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER, product_id INTEGER, quantity INTEGER, ordered_at TEXT);      

    INSERT INTO users (id, name, city, age) VALUES 
        (1, '홍길동', '서울', 30),
        (2, '김철수', '부산', 25),
        (3, '이영희', '대구', 28),
        (4, '박민수', '인천', 32);

    INSERT INTO products (id, name, price, category) VALUES
        (1, '노트북', 1_500_000, '전자제품'),
        (2, '스마트폰', 800_000, '전자제품'),
        (3, '책상', 200_000, '가구'),
        (4, '의자', 100_000, '가구');

    INSERT INTO orders (id, user_id, product_id, quantity, ordered_at) VALUES
        (1, 1, 1, 1, '2026-01-01'),
        (2, 1, 3, 2, '2026-01-05'),
        (3, 2, 2, 1, '2026-02-10'),
        (4, 3, 4, 4, '2026-03-15'),
        (5, 4, 1, 1, '2026-04-20'),
        (6, 4, 2, 2, '2026-05-25');
    """
)

conn.commit()

SCHEMA = """
    users(id, name, city, age)
    products(id, name, price, category) -- price 단위: 원
    orders(id, user_id, product_id, quantity, ordered_at) -- user_id=users.id, product_id=products.id
"""

@tool
def run_sql(query: str) -> str:
    """
    SQLite DB에 SQL 구문을 실행하고 결과를 반환한다.
    """
    q = query.strip().rstrip(';') + ';'  # 세미콜론으로 끝나도록 보장
    cur = conn.execute(q)
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()

    if not rows:
        return "결과가 없습니다."

    # 위 쿼리 결과를 최대한 이쁘게 자연어로 반환하는 코드
    out = [" | ".join(cols)]
    out += [" | ".join(str(v) for v in row) for row in rows]
    return "\n".join(out)

SYSTEM = f"""
    당신은 SQLite 데이터 분석가입니다. 아래 스키마를 사용해서 질문에 답하시오.

    [스키마]
    {SCHEMA}

    [규칙]
    - 답변을 할 때에는 run_sql 툴을 사용해서 쿼리문을 실행하시오.
    - SQLite3 문법만을 사용하고 JOIN, GROUP BY 등도 사용 가능합니다.
"""

llm = ChatOpenAI(model='gpt-4o-mini')
agent = create_agent(llm, tools=[run_sql], system_prompt=SYSTEM)

questions = [
    "서울 사는 사용자는 몇 명인가요?",
    "가장 비싼 상품 3개를 가격이 높은 순으로 보여줘.",
    "홍길동이 주문한 상품 이름과 수량을 보여줘.",
    "카테고리별 총 주문 수량을 알려줘."
]

for q in questions:
    print(f"\n질문: {q}")
    result = agent.invoke({
        "messages": [("user", q)]
    })

    for m in result['messages']:
        for call in getattr(m, 'tool_calls', None) or []:
            print(f" [실행한 쿼리] {call['args'].get('query')}")
    print(f"[답변] {result['messages'][-1].content}\n\n")