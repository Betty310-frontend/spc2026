# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, render_template, make_response

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# set UTF-8 in response headers
@app.after_request
def set_utf8_header(response):
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

@app.route('/', methods=['GET'])
def index():
    return render_template('form.html')

@app.route('/login', methods=['POST'])
def login():
    id = request.form.get('id')
    password = request.form.get('password')
    print(f"입력한 아이디: {id}, 입력한 비밀번호: {password}")
    return render_template('login.html', name=id)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)