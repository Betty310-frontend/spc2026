# 표준 LCEL로 RAG 모델 구현하기

import os
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

load_dotenv()

# 1. 백터 스토어 (DB) 정의
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, 'chroma_db')
DOCS_DIR = os.path.join(BASE_DIR, '.', 'docs')

COLLECTION_NAME = 'my_rag'

embeddings = OpenAIEmbeddings(model='text-embedding-3-small')

store = Chroma(collection_name=COLLECTION_NAME, embedding_function=embeddings, persist_directory=DB_DIR)

if store._collection.count() == 0:
    docs = TextLoader(os.path.join(DOCS_DIR, 'NVMe.txt'), encoding='utf-8').load() \
        + TextLoader(os.path.join(DOCS_DIR, 'HBM.txt'), encoding='utf-8').load()

    chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100).split_documents(docs)
    for chunk in chunks:
        chunk.metadata['source'] = os.path.basename(chunk.metadata.get('source', '?'))

    store.add_documents(chunks)

retriever = store.as_retriever(search_kwargs={'k':3})

# 2. LLM + 프롬프트 설계
llm = ChatOpenAI(model='gpt-4o-mini') # , temperature=0
prompt = ChatPromptTemplate.from_messages([
    ('system', 
     '당신은 문서 기반 QA 시스템입니다. 아래 문서만 참고해서 답변하시오.'
     '문서에 필요한 내용이 없으면 답변할 수 없다고 하시오.'
     '\n\n문서:\n{context}\n'
    ),
    ('user', '{question}')
])

parser = StrOutputParser()

# 3. 표준 질이 응답을 위한 파이프라인 설계 (체이닝)
def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)

def debug_prompt(prompt_input):
    print("\n--- [디버그] LLM에 들어갈 인풋값 ---")
    for msg in prompt_input.messages:
        print(f"[{msg.type.upper()}]")
        print(msg.content[:50] + ('...' if len(msg.content) > 50 else ''))
    print("--- [디버그] 인풋값 끝 ---\n")
    return prompt_input
    

chain = (
    RunnablePassthrough.assign(context=lambda x: format_docs(retriever.invoke(x['question'])))
    | prompt
    | RunnableLambda(debug_prompt) # 디버깅용 람다 함수. 중간 결과 확인 가능
    | llm
    | parser
)

if __name__ == "__main__":
    # 4. 최종 질문 테스트
    print(chain.invoke({'question': 'NVMe와 HBM의 차이는'}))
    print('\n'+'-'*30+'\n')
    print(chain.invoke({'question': '가성비 좋은 패스트 푸드 추천해줘.'}))
    print('\n'+'-'*30+'\n')
    print(chain.invoke({'question': 'NVMe와 HBM 중 어떤 게 더 비싸?'}))