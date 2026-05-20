# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    # Flask나 SQLAlchemy와는 무관함. 파이썬 클래스 출력 시 보기 좋게 출력하기 위한 메서드 
    def __repr__(self):
        return f'<User {self.id}, {self.name}, {self.age}>'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here' # 민감 정보는 .env로 관리 필요
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

db.init_app(app)

# set UTF-8 in response headers
@app.after_request
def set_utf8_header(response):
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

@app.route('/')
def index():
    users = User.query.all()
    for user in users:
        print(user)
    return render_template('index.html', users=users)

@app.route('/add-user', methods=['POST'])
def add_user():
    username = request.form.get('username').strip()
    age = request.form.get('age')

    if not username or not age:
        flash("모든 필드를 입력해주세요.", "error")
        return redirect(url_for('index'))
    
    try:
        age = int(age)
        new_user = User(name=username, age=age)
        db.session.add(new_user)
        db.session.commit()
        flash("유저가 성공적으로 추가되었습니다.", "success")
    except Exception as e:
        print(f"Error adding user: {e}")
        flash("유저 추가 중 오류가 발생했습니다.", "error")

    return redirect(url_for('index'))

@app.route('/delete-user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    try:
        db.session.delete(user)
        db.session.commit()
        flash("유저가 성공적으로 삭제되었습니다.", "success")
    except Exception as e:
        print(f"Error deleting user: {e}")
        flash("유저 삭제 중 오류가 발생했습니다.", "error")

    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        print('DB 초기화 중 ...')
        db.create_all() # 데이터베이스와 테이블 생성

        if not User.query.first(): # 만약 사용자가 한 명도 없다면?
            print('사용자 초기화 중 ...')
            user1 = User(name='user1', age=30)
            user2 = User(name='user2', age=25)
            user3 = User(name='user3', age=34)
            db.session.add_all([user1, user2, user3])
            db.session.commit()

    app.run(debug=True, host='0.0.0.0', port=5000)