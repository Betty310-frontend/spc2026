import os
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, 'chroma_db')
DOCS_DIR = os.path.join(BASE_DIR, '.', 'docs')

embeddings = OpenAIEmbeddings(model='text-embedding-3-small')
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

def build_document(file_path, collection_name):
    store = Chroma(collection_name=collection_name, embedding_function=embeddings, persist_directory=DB_DIR)
    if store._collection.count() > 0: # 지금은 단순 DB라서, 최초 1회만 빌드
        return store
    
    docs = TextLoader(file_path, encoding='utf-8').load()
    chunks = splitter.split_documents(docs)
    for chunk in chunks:
        chunk.metadata['source'] = os.path.basename(file_path)

    return Chroma.from_documents(chunks, embeddings, collection_name=collection_name, persist_directory=DB_DIR)
    
# 1. 컬렉션 2개 준비
collections = {
    'nvme': build_document(os.path.join(DOCS_DIR, 'NVMe.txt'), 'nvme'),
    'hbm': build_document(os.path.join(DOCS_DIR, 'HBM.txt'), 'hbm'),
}

for name, store in collections.items():
    print(f"컬렉션: {name}, 청크 개수: {store._collection.count()}")

# 2. 컬렉션 내 검색
def search_in(name, query, k=2):
    return collections[name].similarity_search(query, k=k)

def search_all(query, k_per=2):
    results = []
    for name, store in collections.items():
        for doc in store.similarity_search(query, k=k_per):
            doc.metadata['collection'] = name # 어느 컬렉션에서 가져왔는지 기록
            results.append(doc)
    return results

# 3. 검색 테스트

query = 'PICe 인터페이스 속도는?'
print(f"\n--- 질문: {query} ---")

print("\n--- 'nvme' 컬렉션 검색 ---")
for doc in search_in('nvme', query):
    print(f"  -> {doc.page_content[:100]}... (출처: {doc.metadata['source']})")

print("\n--- 'nvme, hbm' 모든 컬렉션 검색 ---")
for doc in search_all(query):
    print(f"(출처: {doc.metadata['source']}, 컬렉션: {doc.metadata['collection']})\n")
    print(f"  -> {doc.page_content[:100]}...")
