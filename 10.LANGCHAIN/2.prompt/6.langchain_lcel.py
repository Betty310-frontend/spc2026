import os
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import (
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate, 
    AIMessagePromptTemplate
)

from langchain_openai import ChatOpenAI

from langchain_core.output_parsers import StrOutputParser

load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("당신은 브랜딩 컨텐츠  기획자 입니다."),
    HumanMessagePromptTemplate.from_template(
        "회사를 홍보하기 위한 제공한 상품을 기반으로 캐치프레이즈를 5개 만들어주세요."
        "회사명: {company}, 상품명: {product} "
    )
])

llm = ChatOpenAI(model='gpt-4o-mini')
parser = StrOutputParser()

# LCEL (LangChain Expression Language) 활용
chain = prompt | llm | parser

# inputs = {'company': '삼성전자', 'product': '메모리'}
inputs = {'company': '하이닉스', 'product': 'HBM'}

result = chain.invoke(inputs) # 여기가 핵심. 모든 건 체인을 호출하면서 실행된다.

final_result = {'response': result}
print(final_result)