from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini')

base_prompt = ChatPromptTemplate.from_messages([
    ("system", "다음 한국어를 {language}로 번역해주세요."),
    ("user", "{text}")
])

chain_en = (
    base_prompt.partial(language='english')
    | llm
    | RunnableLambda(lambda x: x.content.strip())
)

chain_ch = (
    base_prompt.partial(language='chinese')
    | llm
    | RunnableLambda(lambda x: x.content.strip())
)

chain_jp = (
    base_prompt.partial(language='japanese')
    | llm
    | RunnableLambda(lambda x: x.content.strip())
)

chain_fr = (
    base_prompt.partial(language='french')
    | llm
    | RunnableLambda(lambda x: x.content.strip())
)

parallel_chain = RunnableParallel({
    'english': chain_en,
    'chinese': chain_ch,
    'japanese': chain_jp,
    'french': chain_fr
})

inputs = {'text': '안녕하세요. 반갑습니다. 당신의 이름은 무엇입니까?'}

result = parallel_chain.invoke(inputs)

print(result)