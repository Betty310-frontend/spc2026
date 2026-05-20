# -*- coding: utf-8 -*-
from flask import Flask, render_template, flash, get_flashed_messages, session, request, redirect, url_for

from datetime import timedelta

import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here' # 민감 정보는 .env로 관리 필요
app.permanent_session_lifetime = timedelta(minutes=5) # 세션 만료 시간 설정
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

DATABASE = 'users.sqlite3' # 데이터베이스 파일명

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row # 모든 데이터를 Dict 포맷으로 관리 ex) row[0] -> row['id']로 접근 가능
    return conn

def init_db():
    with app.app_context(): # Flask 앱 컨텍스트 내에서 데이터베이스 초기화
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL           
            )
        """)

        # 기본 사용자 추가 (username: admin, password: admin)
        cursor.execute("SELECT COUNT(*) AS count FROM users")
        count = cursor.fetchone()['count']
        if count == 0:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('user1', 'password1'))
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('user2', 'password2'))
            conn.commit()

        # 부팅 시 계정 정보 출력
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        
        print('-' * 50)
        for row in rows:
            print(f"ID: {row['id']}, Username: {row['username']}, Password: {row['password']}")
        print('-' * 50)

        conn.close()


# set UTF-8 in response headers
@app.after_request
def set_utf8_header(response):
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            session['user'] = username
            flash('성공적으로 로그인 되었습니다.') # 로그인 메시지 플래시
            return redirect(url_for('home'))
        else:
            flash('로그인에 실패했습니다. 사용자 이름 또는 비밀번호를 확인하세요.') # 로그인 실패 메시지 플래시
            return redirect(url_for('login'))
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    flash('성공적으로 로그아웃 되었습니다.') # 로그아웃 메시지 플래시
    session.pop('user', None) # 세션에서 사용자 정보 제거
    return redirect(url_for('home'))

if __name__ == '__main__':
    init_db() # 데이터베이스 초기화
    app.run(debug=True, host='0.0.0.0', port=5000)