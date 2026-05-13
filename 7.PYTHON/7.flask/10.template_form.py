# -*- coding: utf-8 -*-
import os

from flask import Flask, jsonify, request, render_template, make_response

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

app.config['UPLOAD_FOLDER'] = 'uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXT

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

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if file and allowed_file(file.filename):
        """
        실습 상 사용자가 올린 파일명을 그대로 사용.
        실 서비스라면 사용자가 올린 파일명은 보안상 위험할 수 있으므로, 서버에서 임의의 파일명으로 저장하는 것이 좋음.
        """
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        print(f"파일 업로드 완료: {file_path}")
        return '파일 업로드 완료'
    else:
        # print("업로드 실패: 허용되지 않은 파일 형식")
        return f'{file.filename}은 업로드 실패: 허용되지 않은 파일 형식'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)