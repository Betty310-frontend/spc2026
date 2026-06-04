"""
방법
  1. 사진을 직접 올린다. (base64 인코딩)
  2. 이미지 URL을 주고 읽어가라고 한다.
"""

import os
from dotenv import load_dotenv

from openai import OpenAI

load_dotenv()

# 단발성 실행 시
client = OpenAI()

# image_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Abessinierkater1.jpg/250px-Abessinierkater1.jpg'
# image_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Cat_Eating_Catgrass.jpg/960px-Cat_Eating_Catgrass.jpg'
# image_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/20160730-P1000510_%2828591534890%29.jpg/250px-20160730-P1000510_%2828591534890%29.jpg'
# image_url = 'https://upload.wikimedia.org/wikipedia/commons/d/df/Wingsuit-01.jpg'
# image_url = 'https://file2.nocutnews.co.kr/newsroom/image/2025/09/14/202509141446444133_0.jpg'
image_url = 'https://img1.daumcdn.net/thumb/R1280x0.fpng/?fname=http://t1.daumcdn.net/brunch/service/user/5dXQ/image/pzPK2wjA4MGNatmcQEX5wfQ5VdI.png'

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            'role': 'user',
            'content': [
                {'type': 'text', 'text': '이 이미지 한국어로 설명해줘.'},
                {'type': 'image_url', 'image_url': {'url': image_url}} # <- 이 줄이 핵심
            ]
        }
    ]
)

print(response.choices[0].message.content)