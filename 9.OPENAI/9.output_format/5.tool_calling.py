import os, json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

def get_weather(city):
    weather = {'서울': '맑음, 25도', '부산': '흐림, 22도', 'LA': '화창함, 30도'}
    return weather.get(city, '해당 도시의 날씨 정보가 없습니다.')

tools = [
    {
        'type': 'function',
        'function': {
            'name': 'get_weather',
            'description': '특정 도시의 현재 날씨를 조회한다.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'city': {
                        'type': 'string',
                        'description': '날씨를 조회할 도시 이름'
                    }
                } 
            },
            'required': ['city']
        }
    }
]

prompt = '질문에 대해 json으로만 답변하시오. 답변은 항상 json 형식으로 작성되어야 합니다.'
user_input = '서울의 날씨를 알려주세요.'

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {'role': 'system', 'content': prompt},
        {'role':'user', 'content':user_input}
    ],
    tools=tools,
    # tool_choice='auto' # 모델이 상황에 맞게 도구를 사용할 수 있도록 허용한다. (명시적으로 특정 도구를 지정할 수도 있음
)

message = response.choices[0].message
# print(answer)
if message.tool_calls:
    call = message.tool_calls[0]
    print(f"도구 이름: {call.function.name}")
    print(f"도구에 전달된 입력: {call.function.arguments}")

# prompt += f'\n\n참고자료: {message.content}'

# final_response = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {'role': 'system', 'content': prompt},
#         {'role':'user', 'content':user_input}
#     ],
# )