import os, json

from dotenv import load_dotenv
from openai import OpenAI

from pydantic import BaseModel

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

user_input = '서울의 인구와 면적을 알려주세요.'

class CityInfo(BaseModel):
    name: str
    population: int
    area_km2: float

response = client.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {'role': 'system', 'content':'질문에 대해 json으로만 답변하시오. 답변은 항상 json 형식으로 작성되어야 합니다.'},
        {'role':'user', 'content':user_input}
    ],
    response_format=CityInfo # 파이썬 객체 (클래스) 형태로 반환
)

answer = response.choices[0].message.content

data = CityInfo.model_validate_json(answer) # json 문자열 -> CityInfo 객체로 변환

print(data.name)
print(data.population)
print(data.area_km2)