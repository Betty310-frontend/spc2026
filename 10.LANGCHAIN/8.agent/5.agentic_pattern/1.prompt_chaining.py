from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini')
parser = StrOutputParser()

# [1단계] 리서치 수행 중...
"""
다음 주제에 대해 핵심 사실 5가지를 간결하게 정리해주세요.
"""
research_prompt = ChatPromptTemplate.from_template(
    """
    다음 주제에 대해 핵심 사실 5가지를 간결하게 정리해주세요.

    주제: {topic}
    """
)
research_chain = research_prompt | llm | parser

# [2단계] 게이트 검증 수행 중...
"""
다음 리서치 결과가 적합한지 평가해주세요.
리서치 결과: {}
평가 기준:
    1. 사실 5가지가 올바르게 포함되어 있는가?
    2. 각 사실이 구체적이고 검증 가능한가?
    3. 주제와 관련이 있는가?
결과:
    PASS 또는 FAIL로만 답하고, PASS인 경우 설명을 붙이지 말고, 실패인 경우 이유를 한줄로 설명하시오.
"""
gate_prompt = ChatPromptTemplate.from_template(
    """
    다음 리서치 결과가 적합한지 평가해주세요.
    리서치 결과: 
    - {research}
    
    ---
    평가 기준:
        1. 사실 5가지가 올바르게 포함되어 있는가?
        2. 각 사실이 구체적이고 검증 가능한가?
        3. 주제와 관련이 있는가?
    ---
    결과:
        PASS 또는 FAIL로만 답하고, PASS인 경우 설명을 붙이지 말고, 실패인 경우 이유를 한줄로 설명하시오.
    """
)
gate_chain = gate_prompt | llm | parser

# [3단계] 분석 수행 중...
"""
다음 리서치 결과를 바탕으로 심층 분석 내용을 작성해주세요.
리서치 결과: {}
다음을 포함해주세요:
- 핵심 트랜드 또는 패턴
- 시사점
- 향후 전망
"""
analysis_prompt = ChatPromptTemplate.from_template(
    """
    다음 리서치 결과를 바탕으로 심층 분석 내용을 작성해주세요.

    ---
    리서치 결과: 
    - {research}
    ---
    다음을 포함해주세요:
    - 핵심 트랜드 또는 패턴
    - 시사점
    - 향후 전망
    """
)
analysis_chain = analysis_prompt | llm | parser

# [4단계] 보고서 생성 중...
"""
다음 리서치와 분석된 내용을 바탕으로 간결한 보고서를 작성하시오.
(CEO에게 보고하는 형식, 실무자가 팀장에게 보고하는 형식, 초등학생도 이해할 수 있도록 쉬운 레벨로 등등 상황에 맞게 작성)
리서치: {}
분석: {}
출력형식:
  - 제목
  - 요약 (3줄)
  - 핵심 발견사항
  - 결론
"""
report_prompt = ChatPromptTemplate.from_template(
    """
    다음 리서치와 분석된 내용을 바탕으로 간결한 보고서를 작성하시오.
    (CEO에게 보고하는 형식, 실무자가 팀장에게 보고하는 형식, 초등학생도 이해할 수 있도록 쉬운 레벨로 등등 상황에 맞게 작성)

    ---
    대상: {target_audience}
    
    ---
    리서치: 
    - {research}

    ---
    분석: 
    - {analysis}

    ---
    출력형식:
      - 제목
      - 요약 (3줄)
      - 핵심 발견사항
      - 결론
    """
)
report_chain = report_prompt | llm | parser

def run_chaining_pipeline(topic, target_audience='CEO'):
    # 1단계: 리서치
    print('[1단계] 리서치 수행 중...')
    research = research_chain.invoke({'topic': topic})

    # 2단계: 게이트 검증
    print('[2단계] 게이트 검증 수행 중...')
    gate_result = gate_chain.invoke({'research': research})
    if gate_result.lower() in 'fail':
        print(f'게이트 검증에 실패하여 해당 업무를 재수행합니다.\n이유: {gate_result.strip()}')

    # 3단계: 분석 수행
    print('[3단계] 분석 수행 중...')
    analysis = analysis_chain.invoke({'research': research})

    # 4단계: 보고서 생성
    print('[4단계] 보고서 생성 중...')
    report = report_chain.invoke({'research': research, 'analysis': analysis, 'target_audience': target_audience})

    return report

"""
질문
1. 2026년도 생성형 AI 시장 동향 조사를 해오시오.
"""
topic = "2026년도 생성형 AI 시장 동향 조사를 해오시오."
result = run_chaining_pipeline(topic, '팀장')

print('-' * 60)
print('최종 보고서:')
print('-' * 60)

# 리서치 -> 게이트 검증 -> 분석 -> 보고서 작성
print(result)