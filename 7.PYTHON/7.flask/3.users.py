# -*- coding: utf-8 -*- 
from flask import Flask, jsonify, make_response

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# 응답 헤더에 UTF-8 인코딩 명시
@app.after_request
def set_utf8_header(response):
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

users = [
    {'name': 'Bob', 'age': 30, 'phone': '010-1234-5678'},
    {'name': '김철수', 'age': 25, 'phone': '010-9876-5432'},
    {'name': '이영희', 'age': 28, 'phone': '010-5555-6666'},
    {'name': '김영희', 'age': 28, 'phone': '010-8888-9999'}
]

@app.route('/')
@app.route('/users')
def get_users():
    return jsonify(users) # JSON 형태로 데이터를 반환하는 함수입니다. API 개발 시 자주 사용됩니다.

@app.route('/users/<name>')
def get_user_by_name(name):
    for user in users:
        if user['name'].lower() == name.lower():
            return jsonify(user)
    return jsonify({'error': '사용자를 찾을 수 없습니다.'}), 404

@app.route('/user/<int:age>')
def get_users_by_age(age):
    print(age)
    
    users_by_age = [user for user in users if user['age'] == age]

    if users_by_age:
        return jsonify(users_by_age)
    return jsonify({'error': '사용자를 찾을 수 없습니다.'}), 404

if __name__ == '__main__':
    app.run(debug=True)