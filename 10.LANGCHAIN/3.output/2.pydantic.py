from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from pydantic import BaseModel, Field

load_dotenv()

class MovieReview(BaseModel):
    """
    영화 리뷰 분석 결과
    """
    title: str = Field(description="영화 제목")
    sentiment: str = Field(description="영화에 대한 감성 분류 (긍정, 부정, 중립)")
    score: int = Field(description="영화에 대한 감성 점수 (1-10)")
    summary: str = Field(description="영화 리뷰 요약 (1~2문장)")
    keywords: list[str] = Field(description="핵심 키워드 3개")

llm = ChatOpenAI(model='gpt-4o-mini')

parser = PydanticOutputParser(pydantic_object=MovieReview)
# print(f"{'-'*20} 포멧 명령문 {'-'*20}")
# print(parser.get_format_instructions())

prompt = ChatPromptTemplate.from_template(
    """
        다음 영화 리뷰를 분석해 주세요.
        리뷰: {review}
        {format_instructions}
    """
)

chain = prompt | llm | parser

reviews = [
    "새로운 좀비로 좀비 장르의 변화를 만들어가는 게 볼만. 설정이 특이하니까 지루하지 않게 계속 보게 되는. 연상호 감독이 대단해보임",
    " 마이클 잭슨 일대의 반 정도 보여주는데 127분은 부족했다. 마이클 잭슨의 음악을 들려주기에 극장의 스피커로 부족했다. 마이클 잭슨의 눈부신 모습을 극장의 스크린안에 담기에 부족했다.라스트신을 다른 무대 다른 곡으로 했더라면...",
    "오프라인에서 온라인으로 변화한 패션, 매거진 업계를 그리고 있지만 너무 빠르게 변화하고 있는 환경에서 자신의 자리를 지키기 위해 치열하게 노력하는 모두가 공감할 영화라고 생각함!!",
    " 책 읽으면서 상상했던 우주와 로키가 영상에 펼쳐져서 진짜 너무... 감동적이어서 눈물났음... 원작 팬들은 무조건 극장으로 가라ㅠㅠㅠㅠ 로키야 사랑해",
    "무서운건 개인에 따라 다르겠지만 쫄은 거에 비해 어어엄청 무서운건 아니였음 근데 언제 뭐가 나올지 모르는 긴장과 압박감에 담 걸렸으면 이건 무서운 영화인거겠지... 배우들 연기에 구멍이 하나도 없고 연출도 신박하고 쉴 틈 없이 몰아쳐서 지루할 틈이 없다 4dx로 봤는데 안개랑 물효과가 진짜 나를 살목지로 데려다 놓은 듯한 느낌 무조건 특화관에서 살목지 보는거 추천 나도 4면 스크린x로 또 보러 갈거임"
]

for review in reviews:
    result = chain.invoke({
        'review': review,
        'format_instructions': parser.get_format_instructions()
    })
    print(f"제목: {result.title}")
    print(f"감성: {result.sentiment}")
    print(f"점수: {result.score}")
    print(f"요약: {result.summary}")
    print(f"핵심 키워드: {', '.join(result.keywords)}")
    print('-' * 50)