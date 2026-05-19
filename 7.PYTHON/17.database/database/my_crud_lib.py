import sqlite3

def connect_db():
    conn = sqlite3.connect('example.db')
    return (conn, conn.cursor())

def disconnect_db(conn):
    conn.commit()
    conn.close()

def create_table():
    conn, cursor = connect_db()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    ''')

    disconnect_db(conn)

def insert_user(name, age):
    conn, cursor = connect_db()
    cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', (name, age))

    disconnect_db(conn)

def get_all_users():
    conn, cursor = connect_db()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()

    disconnect_db(conn)
    return users

def get_user_by_name(name):
    conn, cursor = connect_db()
    cursor.execute('SELECT * FROM users WHERE name = ?', (name,))
    users = cursor.fetchall()

    disconnect_db(conn)
    return users

def get_user_by_id(user_id):
    conn, cursor = connect_db()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()

    disconnect_db(conn)
    return user

def update_user(user_id, name=None, age=None):
    conn, cursor = connect_db()

    if name and age:
        cursor.execute('UPDATE users SET name = ?, age = ? WHERE id = ?', (name, age, user_id))
    elif name:
        cursor.execute('UPDATE users SET name = ? WHERE id = ?', (name, user_id))
    elif age:
        cursor.execute('UPDATE users SET age = ? WHERE id = ?', (age, user_id))

    disconnect_db(conn)

def delete_user_by_id(user_id):
    conn, cursor = connect_db()
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    disconnect_db(conn)