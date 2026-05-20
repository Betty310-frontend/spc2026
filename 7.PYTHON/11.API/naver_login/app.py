# -*- coding: utf-8 -*-
from flask import Flask, jsonify, redirect, request, render_template
import requests

from dotenv import load_dotenv
import os

load_dotenv()

NAVER_CLIENT_ID = os.getenv('NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = os.getenv('NAVER_CLIENT_SECRET')
NAVER_AUTHORIZE_URL = os.getenv('NAVER_AUTHORIZE_URL')
NAVER_CALLBACK_URI = os.getenv('NAVER_REDIRECT_URI')
NAVER_TOKEN_URL = os.getenv('NAVER_TOKEN_URL')

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# set UTF-8 in response headers
@app.after_request
def set_utf8_header(response):
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/naver_login')
def naver_login():
    auth_url = (
        f"{NAVER_AUTHORIZE_URL}?"
        f"response_type=code&client_id={NAVER_CLIENT_ID}"
        f"&redirect_uri={NAVER_CALLBACK_URI}&state=HELLO"
    )
    return redirect(auth_url)

@app.route('/api/naver/callback')
def naver_callback():
    code = request.args.get('code')
    state = request.args.get('state')
    
    # code로 네이버에 확인 요청 보내서 access_token 받는 과정 필요
    token_url = (
        f"{NAVER_TOKEN_URL}?grant_type=authorization_code&client_id={NAVER_CLIENT_ID}"
        f"&client_secret={NAVER_CLIENT_SECRET}&code={code}&state={state}"
    )
    
    token_response = requests.get(token_url)
    """
    access_token 받아오기 성공.
    필수동의 항목은 다 받을 수 있고, 선택동의 항목은 유저가 동의한 경우에만 받을 수 있음.
    """

    if token_response.status_code == 200:
        token_data = token_response.json()
        access_token = token_data.get('access_token')
        print('Access Token:', access_token)  # 디버깅용 출력
        return jsonify({'access_token': access_token})
    else:
        return jsonify({'error': 'Failed to obtain access token'}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)