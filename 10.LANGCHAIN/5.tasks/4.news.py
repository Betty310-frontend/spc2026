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
from langchain_core.runnables import RunnableLambda, RunnableParallel

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini')

summary_prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 뉴스 분석 전문가입니다."),
    (
        "user",
        "다음 뉴스 기사를 한국어로 2~3문장으로만 요약해주세요. 불필요한 설명 없이 요약문만 출력하세요.\n\n{news}",
    ),
])

sentiment_prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 뉴스 감정 분석 전문가입니다."),
    (
        "user",
        "다음 뉴스 기사 전체 분위기의 감정을 한 단어로만 출력하세요. 그리고 1문장으로 설명해주세요. 예: 긍정, 부정, 중립\n\n{news}",
    ),
])

category_prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 뉴스 카테고리 분류 전문가입니다."),
    (
        "user",
        "다음 뉴스 기사의 카테고리를 한 단어(또는 짧은 명사구)로만 출력하세요. 예: 연예, 정치, 경제, 사회, 스포츠\n\n{news}",
    ),
])

summary_chain = (
    summary_prompt
    | llm 
    | RunnableLambda(lambda x: x.content.strip())
)

sentiment_chain = (
    sentiment_prompt
    | llm 
    | RunnableLambda(lambda x: x.content.strip())
)

category_chain = (
    category_prompt
    | llm 
    | RunnableLambda(lambda x: x.content.strip())
)

parallel_chain = RunnableParallel({
    'summary': summary_chain,
    'sentiment': sentiment_chain,
    'category': category_chain
})

inputs = {
    "news": """
[마이데일리 = 곽명동 기자]코미디언 김신영이 tvN '유 퀴즈 온 더 블럭'에 출연해 거침없는 입담을 뽐낸다.

지난 27일 방송된 '유 퀴즈 온 더 블럭' 방송 말미에는 다음 주 예고편에 등장한 김신영의 모습이 담겼다.

예고편에서 MC 유재석은 "44kg을 감량했는데 (원래 몸무게로) 돌아오기까지 6주밖에 안 걸렸다고 하더라"라며 말문을 열었다. 이에 김신영은 "초코케이크, 라면, 짜장면, 아이스크림을 마구 먹었더니 바로 살이 쪘다"고 답해 웃음을 자아냈다.

이어 그는 "살이 빠졌을 때는 모든 게 다 불만이었다"라며 극심한 다이어트로 예민했던 과거를 돌이켜보기도 했다. 특히 김신영은 "공황장애가 왔을 때 고(故) 전유성 교수님이 '제발 사람들과 손잡고 다니라'고 말씀하셨다"고 전하며 끝내 눈시울을 붉혀 뭉클함을 안겼다.

한편, 김신영은 과거 88kg에서 44kg까지 감량한 후 약 13년간 몸무게를 유지하며 '다이어트 아이콘'으로 사랑받았다. 최근 다이어트를 포기하고 다시 살을 찌우기 시작한 그의 솔직한 고백에 누리꾼들의 따뜻한 응원이 이어지고 있다.
"""
}

result = parallel_chain.invoke(inputs)

print(f"{'-'*10} 뉴스 요약 {'-'*10}\n")
print(result['summary'])
print(f"\n{'-'*10} 뉴스 감정 분석 {'-'*10}\n")
print(result['sentiment'])
print(f"\n{'-'*10} 뉴스 카테고리 분석 {'-'*10}\n")
print(result['category'])