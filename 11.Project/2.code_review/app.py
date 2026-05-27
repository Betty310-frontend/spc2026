"""
코드 취약점 분석기
1. 코드 입력란 - 사용자가 분석할 코드를 입력할 수 있는 텍스트 영역
2. 분석 버튼 - 사용자가 코드를 분석할 수 있는 버튼
3. 결과 표시 영역 - 분석 결과를 보여주는 영역
"""

from dotenv import load_dotenv
import os

from openai import OpenAI

from flask import Flask, jsonify, request, send_from_directory

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

app = Flask(__name__, static_folder='public')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    # 데이터를 json 형태로 받아온다.
    code = request.json.get('code', '')
    system_prompt = (
        "당신은 숙련된 보안 전문가입니다." 
        "다음 코드를 분석하여 잠재적인 취약점을 찾아내고,"
        "그 취약점이 어떤 위험을 초래할 수 있는지 설명해주세요."
        "각 취약점에 대해 해당 코드의 라인 번호, 코드 스니펫, 취약점 설명, 위험 수준(낮음, 중간, 높음)을 포함한 상세한 분석을 제공해주세요."
    )
    # chatGPT API로 요청
    chat_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system", "content": system_prompt},
            {"role":"user", "content": code}
        ]
    )
    # 결과를 json 형태로 반환
    return jsonify({'result': chat_response.choices[0].message.content})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)