from dotenv import load_dotenv

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

load_dotenv()

llm = ChatAnthropic(model='claude-sonnet-4-6')

template = PromptTemplate.from_template("""
    다음 주제에 대해 설명해주세요.
    ---
    주제: {topic}
    ---
    답변에 이모지 포함 금지. 
    글 문체를 AI티가 안 나게 사람이 쓴 것처럼 최대한 표현해줄 것.
""")

# formatted_prompt = template.format(topic="LLM 기술")
# response = llm.invoke(formatted_prompt)
# print(response.content)

# formatted_prompt = template.format(topic='Transformer 기술')
# response = llm.invoke(formatted_prompt)
# print(response.content)

##############################

chat_template = ChatPromptTemplate.from_messages([
    ('system', '당신은 {role} 전문가 입니다. 질문에 자세히 답변해주세요.'),
    ('user', '다음 개념에 대해서 설명해주세요: {concept}')
])

chain = chat_template | llm

response = chain.invoke({'role':'영화', 'concept': 'Transformer'})
print(response.content)