"""
목적
- 뉴스를 분석한다.
- 뉴스 입력 -> 요약 
          -> 감정 분석 
          -> 카테고리 분석
- RunnableParallel을 활용하여 병렬로 요약, 감정 분석, 카테고리 분석 수행
"""

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini')

parser = StrOutputParser()

# NOTE: chain이란? prompt | llm | parser
summary_prompt = ChatPromptTemplate.from_template(
    '다음 뉴스를 2~3문장으로 요약해 주세요.\n\n{news}'
)
summary_chain = (summary_prompt | llm | parser)

sentiment_prompt = ChatPromptTemplate.from_template(
    '다음 뉴스의 전반적 감성을 한 단어로 분석해줘 (긍정 / 부정 / 중립). 그리고 그 이유를 1문장으로 설명해줘.\n\n{news}'
)
sentiment_chain = (sentiment_prompt | llm | parser)

category_prompt = ChatPromptTemplate.from_template(
    '다음 뉴스의 카테고리를 한 단어로 분석해줘 (정치 / 경제 / 사회 / 문화 / 스포츠 / IT / 기타).\n\n{news}'
)
category_chain = (category_prompt | llm | parser)

final_chain = RunnableParallel({
    "summary": summary_chain,
    "sentiment": sentiment_chain,
    "category": category_chain
})

news = """
서소문 고가차도 붕괴 사고가 난 지 3일 만에 경찰이 강제수사에 착수했습니다.

서울경찰청 광역수사대는 오늘 오전 9시부터 서울도시기반시설본부와 공사 원청·하청업체 본사, 현장 사무실 등 7곳을 대상으로 압수수색을 진행하고 있다고 밝혔습니다.

오늘 압수수색에는 광역범죄수사대원 33명과 서울지방고용노동청 근로감독관 등 모두 53명이 투입됐습니다.

경찰은 압수수색을 통해 확보한 자료를 분석해 사고 원인과 책임 소재를 명확히 규명하겠다고 밝혔습니다.

지난 26일 낮 2시 반쯤 서울 서대구문구에 있는 서소문 고가차도 철거 현장에서 상판 구조물이 무너져 현장관리소장 등 3명이 숨지고 3명이 다쳤습니다.

경찰은 사고 발생 직후 50여 명 규모의 전담수사팀을 꾸리고 현장 정밀 감식에 나섰으며, 서울시로부터 안전관리계획서를 확보하는 등 본격 수사에 나섰습니다.

이용주(tallmoon@mbc.co.kr)
"""

result = final_chain.invoke(news)

print("-" * 50)
print(f"원문: {news[:200]}...")  # 원문이 너무 길 수 있으니 앞부분만 출력
print("-" * 50)
print(f"\n요약: {result['summary']}")
print(f"\n감성: {result['sentiment']}")
print(f"\n카테고리: {result['category']}")