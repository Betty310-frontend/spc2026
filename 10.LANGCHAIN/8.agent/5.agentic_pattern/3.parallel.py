from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

load_dotenv()

parser = StrOutputParser()

# 병렬처리를 통해서 시간을 단축한다.
vote_prompt = ChatPromptTemplate.from_template(
    """
    당신은 번역 품질 평가 전문가입니다. 다음 번역의 품질을 평가해주세요.

    ---
    원문(영어):
    {original}
    ---
    번역(한국어):
    {translation}
    ---
    평가 점수: 1~5점 (리커트 척도)
    평가 점수에 대한 간단한 이유를 1줄로 작성해주세요.
    """
)

llm1 = ChatOpenAI(model='gpt-4o-mini', temperature=0.0)
llm2 = ChatOpenAI(model='gpt-4o-mini', temperature=0.5)
llm3 = ChatOpenAI(model='gpt-4o-mini', temperature=1.0)

voter1 = vote_prompt | llm1 | parser
voter2 = vote_prompt | llm2 | parser
voter3 = vote_prompt | llm3 | parser

parallel_voter = RunnableParallel({
    'voter1': voter1,
    'voter2': voter2,
    'voter3': voter3
})

# 번역 전문 챗봇 솔루션
# 어떻게 하면 번역 품질을 높일 수 있을까?
# 1. 여러 개의 모델을 사용
# 2. Agent를 사용하여 평가하도록 함. (LLM-as-a-judge 기술을 통해서 평가)
# 3. 가장 좋은 선택을 함
def evaluate_translation(original: str, translation: str) -> str:
    results = parallel_voter.invoke({
        'original': original,
        'translation': translation
    })
    return '\n\n'.join(
        f"{name}\n{result}" for name, result in results.items()
    )

# 시험 문장을 넣고, 중간 번역 결과 3개 출력하고,
# 최종 결과물 도출
if __name__ == "__main__":
    original_text = "The quick brown fox jumps over the lazy dog."
    translation_text = "빠른 갈색 여우가 게으른 개를 뛰어넘는다."

    evaluation_result = evaluate_translation(original_text, translation_text)
    print(evaluation_result)