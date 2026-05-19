import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect('example.db')

# 커서 객체 생성, 커서를 통해 실제 데이터 입출력 실행
cursor = conn.cursor()

# 테이블 생성
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY, 
        name TEXT NOT NULL,
        age INTEGER NOT NULL
    )               
''')

conn.commit() # 변경사항 저장
conn.close() # 연결 종료
