import sqlite3

conn = sqlite3.connect('example.db')
cursor = conn.cursor()

cursor.execute('SELECT COUNT(*) FROM users')
count = cursor.fetchone()[0]

if count == 0:
    cursor.execute('''
        INSERT INTO users (name, age) VALUES (?, ?);
    ''', ('Alice', 30))

    cursor.execute('''
        INSERT INTO users (name, age) VALUES (?, ?);
    ''', ('Bob', 25))
    conn.commit()
else:
    print('이미 테이블에 데이터가 존재합니다.')

conn.close()