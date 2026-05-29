import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

from langchain_chroma import Chroma

load_dotenv()

DB_DIR = './chroma_db'
COLLECTION_NAME = 'coding'

embeddings = OpenAIEmbeddings(model='text-embedding-3-small')

def build_store():
    docs = PyPDFLoader('./docs/javascript_secure_coding.pdf').load()
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

results = store.similarity_search("어떻게 코딩하는 것이 안전한가요?", k=3)
for idx, d in enumerate(results, 1):
    print(f"    -> {d.page_content[:60]}...\n")

