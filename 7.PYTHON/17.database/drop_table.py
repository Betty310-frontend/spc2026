import sqlite3

def drop_table():
    # 데이터베이스 연결
    conn = sqlite3.connect('example.db')

    # 커서 객체 생성, 커서를 통해 실제 데이터 입출력 실행
    cursor = conn.cursor()

    # 테이블 삭제
    cursor.execute('''
        DROP TABLE IF EXISTS users
    ''')

    conn.commit() # 변경사항 저장
    conn.close() # 연결 종료

if __name__ == "__main__":
    drop_table()