"""
목적
- 긴 문장을 받아서 짧게 요약한다.
"""


from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
)
from langchain_core.runnables import RunnableLambda

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.5) # 0.3 ~ 0.5

template = "다음의 문장을 3개의 문장으로 요약하시요:\n\n{article}"

chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("당신은 전문 문장 요약가입니다. 긴 문장을 받아서 짧게 요약하는 역할을 합니다."),
    HumanMessagePromptTemplate.from_template(template),
])

chain = chat_prompt | llm | RunnableLambda(lambda x: {'summary': x.content.strip()})

input_text = {
    'article': """[뉴스엔 배효주 기자] 구교환이 본인의 연출작에 전지현을 캐스팅하고 싶다면서 "이미 시나리오가 있다"고 귀띔했다.

영화 '군체'(감독 연상호)에 출연한 구교환은 5월 28일 서울 종로구 모처에서 진행된 인터뷰를 통해 흥행 소감 등을 밝혔다.

지난 21일 개봉한 영화 '군체'는 정체불명의 감염사태로 봉쇄된 건물 안, 고립된 생존자들이 예측할 수 없는 형태로 진화하는 감염자들에 맞서 벌이는 사투를 그린 작품이다.

제79회 칸 국제영화제 미드나잇 스크리닝 부문 공식 초청작이기도 한 '군체'는 프랑스 칸 현지에서 상영된 후 7분 간의 기립박수를 받으며 호평을 이끌어냈다.

개봉 후 단 5일 만에 누적 관객 200만 명을 돌파하며 흥행 중인 가운데, 구교환은 극중 빌런 '서영철' 역을 맡아 강렬한 열연을 펼친다.

'군체'를 통해 호흡한 전지현과 가까운 사이가 된 것에 대해 구교환은 "우리 두 사람 다 유머를 좋아한다. 서로 경쟁하듯이 유머를 뱉어낸다"면서 "친해지는 과정이 없어서 신기했다. 처음 학교에 입학해서 반 배정 됐을 때, '누구랑 친하게 지내야 하나' 스캔을 한 번 하지 않나. 첫 '군체' 모임이 있었을 때 전지현이란 이름을 떼어내고 공정하게 보니 '저 친구, 나랑 유머로 원투펀치가 가능할 거 같다' 싶더라. 재밌는 현장 생활을 할 수 있겠다 싶었다"고 말했다.

전지현의 유머 감각을 평해 달라는 말에 그는 "순발력, 창의성이 있다. 준비해 오지 않고 순간의 아이템으로 던지는 것. 그런 사람이 현장에 세 명 있었는데, 연상호, 전지현, 구교환이다. 그 중 전지현 선배가 가장 재밌다"고 전했다.

앞서 전지현은 구교환을 두고 "여동생 같다"고 표현하기도 했다. 이에 구교환은 "제게 선배님은 현장의 베프, 같은 반 친구, 응원단장 같은 사람"이라며 "오히려 이렇게 친해졌을 때 주인공과 빌런의 관계가 영화 속에서 더 잘 보일 수 있겠다는 생각도 들었다. 연기도 감정으로 하는 안무인데, 두 사람의 취향이 닮아있으니까 적으로 만나는 관계라도 시너지가 오르는 것 같았다"고 덧붙였다.

"제가 좋아하는 사람들은 공통점이 있다. 예상과 똑같다는 것"이라 말한 그는 "제 나름대로 전지현 선배님을 보고 20년 동안 '저 사람은 어떨 것이다' 예상했을 거 아니냐. 제 예상 그대로였다. 미디어에서 표현되지 않은 모습도 근사했다"고 동료애를 드러냈다.

영화감독으로 연출 활동도 하고 있는 그는 "제 영화에 전지현 선배를 출연시키고 싶은 욕심이 있다. 실제로 연상호 감독님이 나오는 시나리오, 전지현 선배님이 나오는 시나리오 다 있다"라며 "하지만 완벽하게 다 쓰기 전까지는 보여드리지 않을 것이다"고 귀띔했다."""
}

result = chain.invoke(input_text)
print("요약\n")
print(result['summary'])