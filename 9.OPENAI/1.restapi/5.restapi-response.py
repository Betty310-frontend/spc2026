import os, requests
from dotenv import load_dotenv

load_dotenv()

openai_response_url = os.getenv('OPENAI_RESPONSE_URL')
openai_api_key = os.getenv('OPENAI_API_KEY')

user_input = "대한민국의 수도는 어디야?"

response = requests.post(
    openai_response_url,
    headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openai_api_key}'
    },
    json={
        'model': 'gpt-4o-mini',
        'input': user_input
    }
)

data = response.json()
print(data)
print('-'*50)
answer = data['output'][0]['content'][0]['text']
print('응답: ', answer)