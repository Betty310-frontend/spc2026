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
llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)
prompt = ChatPromptTemplate.from_messages([
    ('system', '당신은 문서 기반 QA 시스템입니다. 아래 문서만 참고해서 답변하시오.'),
    ('user', '{question}')
])

parser = StrOutputParser()

# 3. 표준 질이 응답을 위한 파이프라인 설계 (체이닝)
def format_docs(docs):
    return "\n\n".join(f"[{i}] {d.page_content}" for i, d in enumerate(docs, start=1))

def extract_sources(docs):
    """
    TODO: 개별 답변 번호화 참고자료 번호 맞추기, 중복 레퍼런스도 허용
    TODO: 이 때 프롬프트에도 명확하게, ex) 답변의 번호화 출처의 답변을 맟춰서 답변하시오
    """
    seen, sources = set(), []
    for d in docs:
        src = d.metadata.get('source', 'N/A')
        if src not in seen: # 참고 문서 중복 제거, 소스를 unique하게 관리하기 위함
            seen.add(src)
            sources.append(src)
    return sources

def retrieve_and_split(inputs):
    docs = retriever.invoke(inputs["question"])
    return {
        "question": inputs["question"],
        "context": format_docs(docs),
        "sources": extract_sources(docs)
    }

def append_sources(docs):
    src_lines = '\n'.join(f" - {s}" for s in docs['sources'])
    return f"{docs['answer']}\n\n참고문서:\n{src_lines}"

chain = (
    RunnableLambda(retrieve_and_split)
    | RunnablePassthrough.assign(answer=(prompt | llm | parser))
    | RunnableLambda(append_sources)
)

# 4. 최종 질문 테스트
question = 'NVMe와 HBM의 차이는?'
print(f"\n--- 질문: {question} ---\n")
print(chain.invoke({'question': question}))

print('\n'+'-'*30+'\n')
question = '가성비 좋은 패스트 푸드 추천해줘.'
print(f"\n--- 질문: {question} ---\n")
print(chain.invoke({'question': question}))
print('\n'+'-'*30+'\n')

question = 'NVMe와 HBM 중 어떤 게 더 비싸?'
print(f"\n--- 질문: {question} ---\n")
print(chain.invoke({'question': question}))