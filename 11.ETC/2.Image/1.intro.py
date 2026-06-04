"""
텍스트를 기반으로 이미지를 생성 (GAN)

구버전 모델이 dall-e => dall-e-2 => ??
현재는 gpt-image-1.5 or gpt-image-2 사용
"""

import base64
from dotenv import load_dotenv

from openai import OpenAI

load_dotenv()

client = OpenAI()

# prompt = "노을 지는 해변, 잔잔한 파도, 수채화 스타일"
prompt = """
노을 지는 해변, 잔잔한 파도, 수채화 스타일,
돌고래 3마리가 파도를 헤엄치다가 그 중 1마리가 점프해서 날개를 달고 날아가면서 하늘을 나는 갈매기를 잡아먹는 모습.
파도는 반짝이는 금빛으로 빛나고, 하늘은 주황색과 보라색이 어우러진 아름다운 노을로 물들어 있다.
공포스러운 분위기와 동시에 아름다운 풍경이 어우러진 장면을 표현해주세요.
"""

result = client.images.generate(
    model='gpt-image-1.5',
    prompt=prompt,
    size='1024x1024', # 1024x1024(정사각형), 1024x1536(세로), 1536x1024(가로)
    quality='high' # low, medium, high, auto (해상도)
)

# image-2
# 4k 해상도 지원 (4096) 16:9 비율도 생성 가능
# 지원 언어 대폭 증가
# 투명 배경 생성 불가

b64 = base64.b64decode(result.data[0].b64_json)
with open("output.png", "wb") as f:
    f.write(b64)

print('이미지 생성 완료: output.png')