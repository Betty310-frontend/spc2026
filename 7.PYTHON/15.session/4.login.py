# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, session, redirect, url_for

# Session은 더 이상 안 함. 실무에서는 사용. -> DB에서 대체

users = [
    {'name':'Alice', 'id':'alice123', 'password':'alicepass'},
    {'name':'Bob', 'id':'bob123', 'password':'bobpass'},
    {'name':'Charlie', 'id':'charlie123', 'password':'charliepass'},
]

app = Flask(__name__)
app.secret_key = 'my-random-key'
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# set UTF-8 in response headers
@app.after_request
def set_utf8_header(response):
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

@app.route('/', methods=['GET'])
def home():
    if session.get('user'):
        return redirect(url_for('welcome'))

    else:
        # 로그인이 아니고, 첫 방문일 때
        return render_template('index.html')
    
@app.route('/dashboard')
def welcome():
    user = session.get('user')
    if user:
        return render_template('dashboard.html', user=user)
    else:
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/', methods=['POST'])
def index():
    # 1. 요청에서 id와 password 추출
    id = request.form.get('id')
    password = request.form.get('password')
    user = None

    # 2. users 리스트에서 id와 password가 일치하는 사용자 찾기
    if id and id.strip() and password and password.strip():
        user = next((u for u in users if u['id'] == id and u['password'] == password), None)

    # 3. 사용자가 있으면
    if user:
        # 4. 세션에 사용자 정보 저장
        session['user'] = user
        error = None
        return redirect(url_for('home'))
    else:
        error = 'Invalid ID or Password'

    return render_template('index.html', error=error)

# 1. 사용자가 비밀번호 바꾸는 기능 추가
# 1-1. method를 POST로 확장
# 1-2. users 안에서 나의 password를 변경
# 1-3. 성공적으로 변경되면 나의 profile에서 확인
# 1-4. '비밀번호 변경'을 눌렀을 때 성공적으로 변경되었음을 알려준다. (사용자 피드백)
def update_password(user):
    new_password = request.form.get('new_pw')
    if new_password and new_password.strip():
        cleaned_password = new_password.strip()
        # session의 user는 복사본일 수 있으므로 원본 users 목록도 함께 갱신한다.
        for saved_user in users:
            if saved_user['id'] == user['id']:
                saved_user['password'] = cleaned_password
                user['password'] = cleaned_password
                break

        session['user'] = user

        return render_template('profile.html', user=user, message='비밀번호가 성공적으로 변경되었습니다.')
    else:
        return render_template('profile.html', user=user, message='새 비밀번호를 입력해주세요.')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    user = session.get('user')
    if user:
        if request.method == 'POST':
            return update_password(user)
        else:
            return render_template('profile.html', user=user)
    else:
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)