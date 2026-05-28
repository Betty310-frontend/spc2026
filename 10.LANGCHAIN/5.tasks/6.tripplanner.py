"""
목적
- 여행 계획을 작성한다.
- 도시 입력 -> 음식 추천
          -> 관광지 추천
          -> 숙박 추천
- 사용자 입력의 OO를 보고 시간표/동선/교통수단 vs 음식/관광지/숙박 추천을 판단하여 분기한다.
- RunnableParallel, RunnableBranch를 활용하여 병렬로 음식 추천, 관광지 추천, 숙박 추천 수행
"""

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnableBranch

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini')

parser = StrOutputParser()

# 음식 추천 체인
food_prompt = ChatPromptTemplate.from_messages([
    ('system', "당신은 여행 음식 추천 전문가입니다. 여행지에서 꼭 먹어야 하는 음식을 추천해주세요."),
    ('user', "다음 도시에서 꼭 먹어야 하는 음식 3가지를 추천해주세요:\n\n{city}"),
])
food_chain = food_prompt | llm | parser

# 관광지 추천 체인
attraction_prompt = ChatPromptTemplate.from_messages([
    ('system', "당신은 여행 관광지 추천 전문가입니다. 여행지에서 꼭 가봐야 하는 관광지를 추천해주세요."),
    ('user', "다음 도시에서 꼭 가봐야 하는 관광지 3곳을 추천해주세요:\n\n{city}"),
])
attraction_chain = attraction_prompt | llm | parser

# 숙박 추천 체인
accommodation_prompt = ChatPromptTemplate.from_messages([
    ('system', "당신은 여행 숙박 추천 전문가입니다. 여행지에서 머물기 좋은 숙박 시설을 추천해주세요."),
    ('user', "다음 도시에서 머물기 좋은 숙박 시설 3곳을 추천해주세요:\n\n{city}"),
])
accommodation_chain = accommodation_prompt | llm | parser

# 도시명 추출 체인
city_extraction_prompt = ChatPromptTemplate.from_messages([
    ("system", "사용자 입력에서 여행 도시명만 추출하세요. 도시명 한 단어만 출력하세요."),
    ("user", "{question}"),
])
city_extraction_chain = city_extraction_prompt | llm | parser

# 시간표/동선/교통수단 일정 체인
itinerary_prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 여행 일정 전문가입니다. 시간표, 동선, 교통수단을 포함해 안내하세요."),
    ("user", "다음 도시의 시간표·동선·교통수단을 포함한 1일 여행 계획을 작성해주세요:\n\n{city}"),
])
itinerary_chain = itinerary_prompt | llm | parser

# 음식/관광지/숙박 병렬 추천 체인
recommendation_chain = RunnableParallel({
    "음식": food_chain,
    "관광지": attraction_chain,
    "숙박": accommodation_chain,
})

# 시간표/동선/교통수단 질문 판단 함수
def is_itinerary_question(x: dict) -> bool:
    question = x.get("question", "")
    return any(k in question for k in ["시간표", "동선", "교통수단", "일정", "코스", "플랜"])


# 분기 체인 (city 키만 추출해서 하위 체인에 전달)
itinerary_runnable = RunnableLambda(lambda x: {"city": x["city"]}) | itinerary_chain
recommendation_runnable = RunnableLambda(lambda x: {"city": x["city"]}) | recommendation_chain

trip_branch = RunnableBranch(
    (is_itinerary_question, itinerary_runnable),
    recommendation_runnable,
)


if __name__ == "__main__":
    user_input = input("여행지와 원하는 정보를 입력하세요\n예) '제주도 시간표 짜줘' / '부산 음식 추천': ")
    city = city_extraction_chain.invoke({"question": user_input})
    data = {"question": user_input, "city": city}
    print(f"\n[추출된 도시] {city}\n")

    result = trip_branch.invoke(data)

    if isinstance(result, dict):
        for key, value in result.items():
            print(f"{'-' * 10} [{key} 추천] {'-' * 10}\n{value}\n")
    else:
        print(f"{'-' * 10} [여행 일정] {'-' * 10}\n{result}")