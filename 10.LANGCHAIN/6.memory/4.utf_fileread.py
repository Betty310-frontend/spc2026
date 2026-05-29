import json
from wcwidth import wcswidth

with open('history.json', 'r', encoding='utf-8') as f:
    messages = json.load(f)

ROLE = {'human': '사용자', 'ai': '챗봇', 'system': '시스템'}

print(f"=== {len(messages)} 메시지 ===")
for idx, message in enumerate(messages, 1):
    role = ROLE.get(message.get('type'), message.get('type'))
    content = message.get('data', {}).get('content', '')
    print(f"{idx:02d}. [{role:<6}] {content}")