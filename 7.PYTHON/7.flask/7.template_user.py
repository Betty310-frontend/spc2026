# -*- coding: utf-8 -*-
from flask import Flask, render_template

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
def main():
    return render_template('users_detail.html', users=users)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)