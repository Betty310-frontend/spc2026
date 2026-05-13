# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, render_template, make_response

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

users = [
    {'name': 'Bob', 'age': 30, 'phone': '010-1234-5678'},
    {'name': '김철수', 'age': 25, 'phone': '010-9876-5432'},
    {'name': '김철수', 'age': 35, 'phone': '010-3255-1234'},
    {'name': '이영희', 'age': 28, 'phone': '010-5555-6666'},
    {'name': '김영희', 'age': 28, 'phone': '010-8888-9999'}
]

# set UTF-8 in response headers
@app.after_request
def set_utf8_header(response):
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

@app.route('/')
def index():
    return {'message': '안녕하세요!'}, 200

@app.route('/search', methods=['GET'])
def search_user():
    """
    쿼리 파라미터로 name, age, phone 으로 검색해서 결과를 반환
    """
    name = request.args.get('name', '')
    age = request.args.get('age', type=int)
    phone = request.args.get('phone', '')
    
    data = []

    for user in users:
        if (name and name.lower() not in user['name'].lower()) or \
            (age and user['age'] != age) or \
            (phone and not user['phone'].startswith(phone)):
                continue
        data.append(user)

    return jsonify({'status': 'success', 'data': data}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)