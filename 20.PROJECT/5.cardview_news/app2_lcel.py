import base64, requests
from bs4 import BeautifulSoup

from dotenv import load_dotenv

from openai import OpenAI
from langchain_openai import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")
client = OpenAI()

def fetch_news(inputs):
    """뉴스 검색 결과를 가져온다."""
    url = "https://news.google.com/rss/search"
    params = {
        "q": inputs['query'],
        "hl": "ko",
        "gl": "KR",
        "ceid": "KR:ko"
    }

    xml = requests.get(url, params=params, timeout=10).text
    soup = BeautifulSoup(xml, "xml")

    items = []
    for item in soup.find_all("item")[:8]:
        items.append({
            "title": item.title.text,
            "link": item.link.text,
            "date": item.pubDate.text
        })
    return str(items)

def make_image_prompt(summary):
    prompt = f"""
        다음 뉴스 요약 내용을 바탕으로 웹툰형 카드뉴스 이미지 생성 프롬프트를 만드시오.

        조건:
        - 한 장짜리 이미지
        - 여러 컷 웹툰 스타일
        - 한국어 텍스트 포함
        - 날짜가 있다면, 각 날짜별로 패널을 구성
        - 뉴스 카드 + 만화 컷 + 인포그래픽 형태로 혼합 구성
        - 인물은 실제 해당 유명인을 캐릭터화 한 느낌으로 생성
        - 회사 로고나 상표 등을 적절하게 활용해서 실제 내용을 살림

        뉴스 요약:
        {summary}
    """

    result = llm.invoke(prompt)
    return result.content

def generate_image(inputs, output="output.png"):
    result = client.images.generate(
        model="gpt-image-1.5",
        prompt=inputs['image_prompt'],
        size="1024x1536",
        quality="medium"
    )

    image_base64 = result.data[0].b64_json
    with open(output, "wb") as f:
        f.write(base64.b64decode(image_base64))

    return output

parser = StrOutputParser()

summarize_chain = (
    ChatPromptTemplate.from_messages([
        ("system", "너는 뉴스 요약 전문가다. 수집된 뉴스 목록을 바탕으로 일정/날짜/행사/만남 정보를 중심으로 간결하게 요약하시오."),
        ("human", "다음 뉴스로 요약해라. {news}")
    ])
    | llm
    | parser
)

image_prompt_chain = make_image_prompt | parser

pipeline = (
    RunnablePassthrough.assign(news=fetch_news)
    | RunnablePassthrough.assign(summary=summarize_chain)
    | RunnablePassthrough.assign(image_prompt=image_prompt_chain)
    | RunnablePassthrough.assign(image_path=generate_image)
)

def main():
    result = pipeline.invoke({"query": "젠슨 황 4박 5일 한국 방문 일정 뉴스들을 조사해줘"})
    print(f"요약: {result['summary']}")
    print(f"이미지 프롬프트: {result['image_prompt']}")
    print(f"생성된 이미지 경로: {result['image_path']}")

if __name__ == "__main__":
    main()