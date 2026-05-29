# javascript_secure_coding.pdf 문서는 한국인터넷진흥원(KISA)에서 제공하는 시큐어 코딩 가이드입니다.
# https://www.kisa.or.kr/2060204/form?postSeq=14&page=1#fnPostAttachDownload

import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from langchain_chroma import Chroma

load_dotenv()

DB_DIR = './chroma_db'
COLLECTION_NAME = 'coding'

embeddings = OpenAIEmbeddings(model='text-embedding-3-small')

def build_store():
    docs = PyPDFLoader('./javascript_secure_coding.pdf').load()
    chunks = RecursiveCharacterTextSplitter(
        chunk_size=2000, chunk_overlap=500
    ).split_documents(docs)
    store = Chroma.from_documents(
        chunks, embeddings, 
        collection_name=COLLECTION_NAME, 
        persist_directory=DB_DIR
    )
    return store

def load_store():
    store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=DB_DIR
    )
    print(f"기존 DB 로딩 성공 - {store._collection.count()} 개의 청크 로딩됌.")
    return store

if os.path.exists(DB_DIR):
    store = load_store()
else:
    store = build_store()

retriever = store.as_retriever(search_kwargs={"k":3})

llm = ChatOpenAI(model='gpt-4o-mini')

parser = StrOutputParser()

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "당신은 문서 기반 Q&A 시스템입니다. 아래 문서만을 참고해서 답하세요. 문서에 적합한 내용이 없으면, '모릅니다'라고 답하세요.\n\n문서:\n{context}"),
        ('user', "{question}")
    ]
)

def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)

chain = (
    RunnablePassthrough.assign(context=lambda x: format_docs(retriever.invoke(x['question'])))
    | prompt
    | llm
    | parser
)

print(chain.invoke({'question': '어떻게 코딩하는 것이 안전한가요?'}))
print("\n" + "="*50 + "\n")
print(chain.invoke({'question': 'HBM이란 무엇인가요?'}))
print("\n" + "="*50 + "\n")
print(chain.invoke({'question': '그걸 왜 모르는데?'}))