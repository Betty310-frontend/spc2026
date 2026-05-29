# pip install chromadb
# pip install langchain-chroma

import os
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

from langchain_chroma import Chroma

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, 'chroma_db')
DOCS_DIR = os.path.join(BASE_DIR, 'docs')
COLLECTION_NAME = 'coding'

embeddings = OpenAIEmbeddings(model='text-embedding-3-small')

def build_store():
    docs = TextLoader(os.path.join(DOCS_DIR, 'HBM.txt'), encoding='utf-8').load()
    chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100).split_documents(docs)
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

# results = store.similarity_search("HBM이란 무엇인가요?", k=2)
results = store.similarity_search("HBM의 성능은 어떤가요?", k=3)
for idx, d in enumerate(results, 1):
    print(f"    -> {d.page_content[:60]}...\n")

