# -*- coding: utf-8 -*-
from flask import Flask, session
from flask_session import Session # 서버 측에 세션을 저장하기 위한 확장 모듈

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.secret_key = 'your_secret_key_here'  # 세션 암호화에 사용되는 비밀 키, 나만 아는 값으로 설정 필요

# 서버 측 세션 설정
app.config['SESSION_TYPE'] = 'filesystem'  # 세션을 파일 시스템에 저장 / 다른 옵션: 'redis', 'memcached', 'mongodb' 등
app.config['SESSION_FILE_DIR'] = './.sessions' # 내가 정한 폴더명
app.config['SESSION_PERMANENT'] = False # 세션이 영구적이지 않도록 설정 (브라우저 종료 시 세션 삭제)
app.config['SESSION_USE_SIGNER'] = True # 세션 ID를 암호화하여 보안 강화

Session(app)

# set UTF-8 in response headers
@app.after_request
def set_utf8_header(response):
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

@app.route('/')
def main():
    if 'username' in session:
        return f"세션에서 당신의 정보를 찾았습니다. {session['username']}, {session['fullname']}, {session['dob']}, {session['hobby']}"
    else:
        session['username'] = 'spc2026'
        session['fullname'] = '홍길동'
        session['dob'] = '2020/05/05'
        session['hobby'] = '유튜브 시청, 쇼핑, 게임'
        return '세션이 설정되었습니다.'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)