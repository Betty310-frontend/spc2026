# -*- coding: utf-8 -*-
from flask import Flask, session

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.secret_key = 'your_secret_key'

# set UTF-8 in response headers
@app.after_request
def set_utf8_header(response):
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

@app.route('/set-session')
def set_session():
    session['username'] = 'spc2026'
    return '세션이 설정되었습니다.'

@app.route('/get-session')
def get_session():
    if 'username' in session:
        return f"세션에서 당신의 정보를 찾았습니다. {session['username']}"
    else:
        return '세션에 정보가 없습니다.'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)