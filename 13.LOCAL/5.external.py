"""
Ollama 서버가 외부에 있는 경우,
나의 request를 API에 요청하듯이 할 수 있음.
"""

from urllib import response

import requests

OLLAMA_HOST = 'http://127.0.0.1:11434'  # 실제 Ollama 서버의 IP 주소와 포트로 변경
OLLAMA_ENDPOINT = f"{OLLAMA_HOST}/api/generate"

payload = {
    'model': 'exaone3.5:2.4b',
    'prompt': '파이썬으로 구현하는 헬로우 월드 예제 코드를 보여줘',
    'stream': False,  # 스트리밍 응답이 필요한 경우 True로 설정
}

response = requests.post(OLLAMA_ENDPOINT, json=payload)
data = response.json()

print(f"모델응답: {data.get('response')}"               )