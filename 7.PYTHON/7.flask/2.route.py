from flask import Flask

app = Flask(__name__)

@app.route('/user')
@app.route('/user/<username>') # <변수명> 형태로 URL 경로에 변수를 지정할 수 있습니다.
def show_user_profile(username='게스트'):
    return f'<h1>사용자: {username}</h1>'

@app.route('/admin')
def show_admin_profile():
    return '관리자: 홍길동'

@app.route('/product')
@app.route('/product/<int:id>') # <int:변수명> 형태로 URL 경로에 정수형 변수를 지정할 수 있습니다.
def show_product(id=0):
    return f'제품코드: {id}, 제품명: 사과'

if __name__ == '__main__':
    app.run(debug=True)