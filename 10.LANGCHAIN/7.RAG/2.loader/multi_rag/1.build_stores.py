import os
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, 'chroma_db')
DOCS_DIR = os.path.join(BASE_DIR, '..', 'docs')

embeddings = OpenAIEmbeddings(model='text-embedding-3-small')

# 각 컬렉션 설정
COLLECTIONS = {
    'hbm': {
        'loader': TextLoader(os.path.join(DOCS_DIR, 'HBM.txt'), encoding='utf-8'),
        'chunk_size': 500,
        'chunk_overlap': 100,
    },
    'nvme': {
        'loader': TextLoader(os.path.join(DOCS_DIR, 'NVMe.txt'), encoding='utf-8'),
        'chunk_size': 500,
        'chunk_overlap': 100,
    },
    'js_secure': {
        'loader': PyPDFLoader(os.path.join(DOCS_DIR, 'Javascript_secure_coding.pdf')),
        'chunk_size': 2000,
        'chunk_overlap': 500,
    },
}

def build_store(name, config):
    """문서를 로딩 후 청킹하여 Chroma 컬렉션에 저장"""
    print(f"[{name}] 문서 로딩 중...")
    docs = config['loader'].load()
    print(f"[{name}] 총 {len(docs)} 페이지 로딩 완료")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config['chunk_size'],
        chunk_overlap=config['chunk_overlap']
    )
    chunks = splitter.split_documents(docs)
    print(f"[{name}] {len(chunks)} 개의 청크로 분할 완료")

    store = Chroma.from_documents(
        chunks,
        embeddings,
        collection_name=name,
        persist_directory=DB_DIR
    )
    print(f"[{name}] 컬렉션 저장 완료 ✅\n")
    return store

def load_store(name):
    """기존 Chroma 컬렉션 로딩"""
    store = Chroma(
        collection_name=name,
        embedding_function=embeddings,
        persist_directory=DB_DIR
    )
    count = store._collection.count()
    print(f"[{name}] 기존 컬렉션 로딩 완료 - {count} 개의 청크 ✅")
    return store

def get_store(name):
    """컬렉션 존재 여부 확인 후 로딩 또는 새로 빌드"""
    store = Chroma(
        collection_name=name,
        embedding_function=embeddings,
        persist_directory=DB_DIR
    )
    if store._collection.count() > 0:
        return load_store(name)
    else:
        return build_store(name, COLLECTIONS[name])

if __name__ == '__main__':
    print("=" * 50)
    print("📦 Chroma 벡터 DB 구축 시작")
    print(f"📁 DB 저장 경로: {DB_DIR}")
    print("=" * 50 + "\n")

    stores = {}
    for name in COLLECTIONS:
        stores[name] = get_store(name)

    print("\n" + "=" * 50)
    print("✅ 전체 컬렉션 구축 완료!")
    print("=" * 50)
    print("\n[유사도 검색 테스트]")

    # 각 컬렉션 검색 테스트
    tests = {
        'hbm': 'HBM이란 무엇인가요?',
        'nvme': 'NVMe의 특징은 무엇인가요?',
        'js_secure': '안전한 자바스크립트 코딩 방법은?',
    }
    for name, question in tests.items():
        print(f"\n🔍 [{name}] 질문: {question}")
        results = stores[name].similarity_search(question, k=2)
        for r in results:
            print(f"    → {r.page_content[:80]}...")
