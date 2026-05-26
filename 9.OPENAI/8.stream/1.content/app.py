"""
openai 기본 틀 불러오기 (dotenv)
flask 기본 틀 짜기
"""

import os 
from dotenv import load_dotenv

from openai import OpenAI

from flask import Flask, json, request, send_from_directory, Response

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=openai_api_key)
app = Flask(__name__, static_folder="public")

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/stream', methods=['POST'])
def stream():
    user_message = request.json.get('message', '')

    # OpenAI API 호출
    def generate_response():
        # 아래 코드도 try-except로 감싸서 에러 처리하는 것이 좋다. 지금은 생략
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 친절한 AI 도우미입니다."},
                {"role": "user", "content": user_message}
            ],
            stream=True
        )
        for chunk in response:
            delta = chunk.choices[0].delta
            content = delta.content or ""
            
            if content:
                yield f"data: {json.dumps({'content': content}, ensure_ascii=False)}\n\n"

    return Response(generate_response(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)