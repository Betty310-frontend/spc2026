# 1. 프롬프트 생성
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 브랜드 기획자 입니다."),
    ("user", 
        "회사를 홍보하기 위한 캐치프레이즈를 5개 만들어주세요. "
        "회사명: {company}, 상품명: {product}"
        "출력 결과는 콤마로 구분된 리스트(CSV) 형태로 작성해주세요."
    )
])

filled_prompt = prompt.format_messages(company='테슬라', product='Model S')

# 2. LLM 모델 호출
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini')
response = llm.invoke(filled_prompt)
print(f'LLM 응답: {response.content}')

# 3. 출력 파서 (Output Parser) 활용
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import CommaSeparatedListOutputParser

parser1 = StrOutputParser()
parser2 = CommaSeparatedListOutputParser()

result_str = parser1.parse(response.content)
result_csv = parser2.parse(response.content)

print('-' * 50)
print(result_str)
print('-' * 50)
print(result_csv)

# 1. 입력정의 (Prompt) => 2.LLM => 3. 결과파싱