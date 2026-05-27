import os, json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

user_input = '서울의 인구와 면적을 알려주세요.'

# NOTE: 내가 원하는 출력 형식 - 즉 자료구조를 정의 (json_schema 정의)
city_schema = {
    "type": "object",
    "properties": {
        "name": {"type":"string"},
        "population": {"type":"integer"},
        "area_km2": {"type":"number"}
    },
    "required": ["name", "population", "area_km2"], # 이 필드는 꼭 채울 것
    "additionalProperties": False, # 정의 하지 않은 건 추가하지 말 것
}

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {'role': 'system', 'content':'질문에 대해 json으로만 답변하시오. 답변은 항상 json 형식으로 작성되어야 합니다.'},
        {'role':'user', 'content':user_input}
    ],
    response_format={
        'type': 'json_schema', 
        'json_schema': {
            'name': 'city_info', # 내가 정의하는 이름
            'strict': True, # 엄격하게 스키마를 지킬 것인지
            'schema': city_schema
        }
    } # 출력 결과가 내가 정의한 스키마로 정의되도록 요청
)

answer = response.choices[0].message.content
# print(answer)

data = json.loads(answer)
print(f"도시의 이름: {data['name']}")
print(f"도시의 인구: {data['population']}")
print(f"도시의 면적: {data['area_km2']} km²")