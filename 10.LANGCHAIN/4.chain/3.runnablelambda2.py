from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, CommaSeparatedListOutputParser
from langchain_core.runnables import RunnableLambda

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini')

prompt1 = ChatPromptTemplate.from_template(
    "{product}을/를 만드는 회사의 이름을 하나 추천해주세요."
)
chain1 = prompt1 | llm | StrOutputParser()
result1 = chain1.invoke({'product': '웹 게임'})

print(f"타입: {type(result1)}, \n결과: {result1}")

print('-' * 50)

prompt2 = ChatPromptTemplate.from_template(
    "{topic}에 관련된 키워드를 5개만 쉼표로 구분해서 나열해주세요."
)
chain2 = prompt2 | llm | CommaSeparatedListOutputParser()
result2 = chain2.invoke({'topic':'인공지능'})
print (f"타입: {type(result2)}, \n결과: {result2}")

print('-' * 50)

# 위 2개의 다른 체인들을 LCEL로 묶어서 한번에 실행해보기
prompt_name = ChatPromptTemplate.from_template(
    "{product}을/를 만드는 회사의 이름을 하나 추천해주세요. 이름만 알려주세요."
)
prompt_slogan = ChatPromptTemplate.from_template(
    "{company_name} 회사의 캐치프레이즈를 만들어주세요. 캐치프레이즈만 알려주세요."
)

chain1 = (
    # 사용자 입력 처리
    prompt_name 
    | llm 
    | StrOutputParser() 
    | RunnableLambda(lambda name: {'company_name': name.strip()}) 
    # 결과를 받아서 2번째 체인 실행
    | prompt_slogan 
    | llm 
    | StrOutputParser()
    | RunnableLambda(lambda slogan: {"slogan": slogan.strip()})
)
result1 = chain1.invoke({'product':'친환경 에코백'})
print(f"타입: {type(result1['slogan'])}, \n결과: {result1['slogan']}")


chain2 = (
    # 사용자 입력 처리
    prompt_name 
    | llm 
    | StrOutputParser() 
    | RunnableLambda(lambda name: {'company_name': name.strip()}) 
    # 2번째 체인
    | RunnableLambda(lambda d: {
        'company_name': d['company_name'],
        'slogan': (
            prompt_slogan | llm | StrOutputParser()
        ).invoke({'company_name': d['company_name']}).strip()
    })
)

print('-' * 50)
result2 = chain2.invoke({'product':'친환경 에코백'})
print(f"결과: {result2}")