from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html>
        <head>
            <title>Flask Intro</title>
            <style>
                p {
                    color: red;
                }
            </style>
        </head>
        <body>
            <h1>Welcome to Flask!</h1>
            <p>This is a simple Flask application.</p>
            <p>Visit <a href="/hello">/hello</a> to see a greeting message.</p>
        </body>
    </html>
    """

@app.route('/hello')
def hello():
    return '<h1>안녕하세요! Flask입니다!</h1>'

if __name__ == '__main__':
    app.run()
# debug=True 옵션은 개발 단계에서만 사용해야 합니다. 배포 시에는 반드시 제거해야 합니다.
