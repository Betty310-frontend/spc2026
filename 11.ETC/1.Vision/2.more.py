"""
방법
  1. 사진을 직접 올린다. (base64 인코딩)
  2. 이미지 URL을 주고 읽어가라고 한다.
"""

import base64
from dotenv import load_dotenv

from openai import OpenAI

load_dotenv()

# 단발성 실행 시
client = OpenAI()

# image_url = '../img/bonobono_ppt.png'
image_url = '../img/juga.jpg'

def encode_image(path):
    with open(path, 'rb') as file:
        return base64.b64encode(file.read()).decode('utf-8')

def ask_about_img(question, b64):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                'role': 'user',
                'content': [
                    {'type': 'text', 'text': question},
                    {'type': 'image_url', 'image_url': {'url': f'data:image/png;base64,{b64}'}} # <- 이미지 유형에 따라 인코딩 된 포맷 바꿔서 설정
                ]
            }
        ]
    )

    return response.choices[0].message.content

questions = [
    # '이미지에 있는 한글 글자 모두 읽어줘.',
    # '해당 이미지에 사용된 주요 색상 알려줘.',
    # '이미지의 전체 분위기를 한 문장으로 표현해줘.',
    '이미지를 한국어로 자세히 설명해줘.',
    '이 주식 차트를 보고 기술적 분석을 해줘.',
    '골든 크로스와 데드 크로스 시점을 알려줘.',
    '매수 또는 매도 타이밍을 분석하고 이유를 설명해줘.'
]

b64_image = encode_image(image_url)

for question in questions:
    print('-' * 60)
    print(f'[질문] {question}')
    answer = ask_about_img(question, b64_image)
    print(f'[답변] {answer}')