"""
multi_rag/2.rag_query.py

사용법:
  python 2.rag_query.py                  # 대화형 모드 (자동 라우팅)
  python 2.rag_query.py --mode all       # 전체 컬렉션 병합 검색
  python 2.rag_query.py --mode hbm       # hbm 컬렉션만 검색
  python 2.rag_query.py --mode nvme      # nvme 컬렉션만 검색
  python 2.rag_query.py --mode js_secure # js_secure 컬렉션만 검색
"""

import os
import argparse
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, 'chroma_db')

embeddings = OpenAIEmbeddings(model='text-embedding-3-small')
llm = ChatOpenAI(model='gpt-4o-mini')
parser = StrOutputParser()

# ── 컬렉션별 키워드 (자동 라우팅에 사용) ──────────────────────────────────
ROUTING_KEYWORDS = {
    'hbm':       ['hbm', '고대역폭', '메모리', 'bandwidth', '적층', 'dram'],
    'nvme':      ['nvme', 'ssd', '스토리지', 'storage', '낸드', 'nand', 'pcie', '플래시'],
    'js_secure': ['자바스크립트', 'javascript', '보안', 'secure', 'xss', 'injection',
                  '취약점', '시큐어', 'csrf'],
}

# ── 프롬프트 ──────────────────────────────────────────────────────────────
PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "당신은 문서 기반 Q&A 시스템입니다.\n"
     "아래 문서 내용만을 참고하여 답변하세요.\n"
     "문서에 관련 내용이 없으면 '제공된 문서에서 해당 내용을 찾을 수 없습니다.'라고 답하세요.\n\n"
     "문서:\n{context}"),
    ("user", "{question}")
])

# ── 유틸 ─────────────────────────────────────────────────────────────────
def load_store(name: str) -> Chroma:
    store = Chroma(
        collection_name=name,
        embedding_function=embeddings,
        persist_directory=DB_DIR
    )
    count = store._collection.count()
    if count == 0:
        raise RuntimeError(
            f"컬렉션 '{name}'이 비어 있습니다. 먼저 1.build_stores.py를 실행하세요."
        )
    return store

def format_docs(docs) -> str:
    return "\n\n".join(d.page_content for d in docs)

def build_chain(retriever):
    return (
        RunnablePassthrough.assign(
            context=lambda x: format_docs(retriever.invoke(x['question']))
        )
        | PROMPT
        | llm
        | parser
    )

# ── 라우팅 ────────────────────────────────────────────────────────────────
def detect_collection(question: str) -> str | None:
    """질문 키워드를 분석해 가장 적합한 컬렉션 이름을 반환. 판단 불가 시 None 반환."""
    q_lower = question.lower()
    scores = {name: 0 for name in ROUTING_KEYWORDS}
    for name, keywords in ROUTING_KEYWORDS.items():
        for kw in keywords:
            if kw in q_lower:
                scores[name] += 1
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else None

# ── 검색 모드 ─────────────────────────────────────────────────────────────
def query_single(name: str, question: str):
    """단일 컬렉션 검색"""
    print(f"\n🔍 [{name}] 컬렉션 검색 중...")
    store = load_store(name)
    retriever = store.as_retriever(search_kwargs={"k": 3})
    chain = build_chain(retriever)
    return chain.invoke({'question': question})

def query_all(question: str):
    """3개 컬렉션 병합 검색 (각 컬렉션 결과를 합산)"""
    print("\n🔍 [전체 컬렉션 병합] 검색 중...")
    all_docs = []
    for name in ['hbm', 'nvme', 'js_secure']:
        retriever = load_store(name).as_retriever(search_kwargs={"k": 2})
        all_docs.extend(retriever.invoke(question))

    context = format_docs(all_docs)
    chain = PROMPT | llm | parser
    return chain.invoke({'question': question, 'context': context})

def query_auto(question: str):
    """키워드 기반 자동 라우팅"""
    detected = detect_collection(question)
    if detected:
        print(f"🤖 자동 라우팅 → [{detected}] 컬렉션 선택")
        return query_single(detected, question)
    else:
        print("🤖 자동 라우팅 → 관련 컬렉션을 특정할 수 없어 전체 병합 검색 실행")
        return query_all(question)

# ── 대화형 루프 ───────────────────────────────────────────────────────────
def interactive_loop(mode: str):
    print("\n" + "=" * 60)
    print("💬 RAG 질의응답 시스템")
    print(f"   모드: {mode}")
    print("   종료하려면 'q' 또는 'exit' 입력")
    print("=" * 60)

    while True:
        question = input("\n질문: ").strip()
        if not question:
            continue
        if question.lower() in ('q', 'exit', 'quit'):
            print("종료합니다.")
            break

        try:
            if mode == 'all':
                answer = query_all(question)
            elif mode == 'auto':
                answer = query_auto(question)
            else:
                answer = query_single(mode, question)

            print(f"\n📝 답변:\n{answer}")
            print("-" * 60)
        except RuntimeError as e:
            print(f"❌ 오류: {e}")
            break

# ── 진입점 ────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    VALID_MODES = ['auto', 'all', 'hbm', 'nvme', 'js_secure']

    arg_parser = argparse.ArgumentParser(description='Multi-collection RAG Query')
    arg_parser.add_argument(
        '--mode', default='auto',
        choices=VALID_MODES,
        help=f"검색 모드 선택: {VALID_MODES} (기본값: auto)"
    )
    args = arg_parser.parse_args()

    interactive_loop(args.mode)
