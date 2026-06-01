# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv

from flask import Flask, jsonify, request, render_template

# 랭체인 기본 세팅
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

# 문서 파서 기본 세팅 (PyPDFLoader)
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

load_dotenv()

# 1. 벡터스토어 셋업
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, 'chroma_db')
COLLECTION_NAME = 'pdf_rag_db'

embedding = OpenAIEmbeddings(model="text-embedding-3-small")
store = Chroma(collection_name=COLLECTION_NAME, embedding_function=embedding, persist_directory=DB_DIR)

def load_and_store(file_path):
    """
    업로드된 PDF 파일을 로드하여 벡터스토어에 저장하는 함수입니다."""
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    if not docs:
        raise ValueError('PDF에서 페이지를 읽지 못했습니다.')

    for d in docs:
        d.metadata['source'] = os.path.basename(file_path)

    chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100).split_documents(docs)
    chunks = [c for c in chunks if c.page_content and c.page_content.strip()]

    if not chunks:
        raise ValueError('PDF에서 텍스트를 추출하지 못했습니다. 스캔본(이미지) PDF일 수 있습니다.')

    store.add_documents(chunks)
    return len(chunks)

# 2. 랭체인 셋업 (LCEL)
llm = ChatOpenAI(model='gpt-4o-mini')
prompt = ChatPromptTemplate.from_messages([
    ('system', 
     '당신은 문서 기반 QA 시스템입니다. 아래 문서만 참고해서 질문에 답하시오.'
     '간결하게 정보만 알려주시오.' 
     '문저에 적합한 내용이 없으면 답변할 수 없다고 하시오.'
     '\n\n문서:\n{context}\n'
    ),
    ('user', '{question}')
])

parser = StrOutputParser()

def format_docs(docs):
    return "\n\n".join(f"[{i}] {d.page_content}" for i, d in enumerate(docs, start=1))

def extract_sources(docs):
    """
    검색된 문서의 출처와 내용을 참고번호와 함께 반환합니다.
    각 참고 항목은 최대 50자로 제한합니다.
    """
    refs = []
    seen = set()

    for i, doc in enumerate(docs, start=1):
        source = doc.metadata.get('source', '알 수 없음')
        # 줄바꿈/여러 공백을 정리해 짧은 참고문구를 만듭니다.
        content = " ".join(doc.page_content.split())
        ref_text = f"[{i}] {source} | {content}"[:50]

        if ref_text not in seen:
            seen.add(ref_text)
            refs.append(ref_text)

    return refs

def retrieve_diverse_docs(question, k_total=6, fetch_k=24, max_per_source=2):
    """
    하나의 source에 결과가 몰리지 않도록 source별 최대 청크 수를 제한해 검색합니다.
    """
    docs = store.similarity_search(question, k=fetch_k)
    if not docs:
        return []

    selected = []
    source_counts = {}

    for doc in docs:
        source = doc.metadata.get('source', '알 수 없음')
        count = source_counts.get(source, 0)
        if count >= max_per_source:
            continue

        selected.append(doc)
        source_counts[source] = count + 1

        if len(selected) >= k_total:
            break

    # max_per_source 제한으로 k_total을 채우지 못한 경우, 남은 문서를 점수 순으로 보충
    if len(selected) < k_total:
        selected_ids = {id(d) for d in selected}
        for doc in docs:
            if id(doc) in selected_ids:
                continue
            selected.append(doc)
            if len(selected) >= k_total:
                break

    return selected

def retrieve_and_split(inputs):
    docs = retrieve_diverse_docs(inputs['question'])
    return {
        'question': inputs['question'],
        'context': format_docs(docs),
        'sources': extract_sources(docs)
    }

def append_sources(docs):
    src_lines = "\n".join(f"- {s}" for s in docs['sources'])
    return f"{docs['answer']}\n\n참고문서:\n{src_lines}"

def debug_prompt(prompt_input):
    print("\n--- [디버그] LLM에 들어갈 인풋값 ---")
    for msg in prompt_input.messages:
        print(f"[{msg.type.upper()}]")
        print(msg.content[:50] + ('...' if len(msg.content) > 50 else ''))
    print("--- [디버그] 인풋값 끝 ---\n")
    return prompt_input

chain = (
    RunnableLambda(retrieve_and_split)
    | RunnablePassthrough.assign(answer=(
        prompt 
        | RunnableLambda(debug_prompt) # 디버깅용 람다 함수. 중간 결과 확인 가능
        | llm 
        | parser
    ))
    |RunnableLambda(append_sources)
)

# 3. FLASK 기본 세팅
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# set UTF-8 in response headers
@app.after_request
def set_utf8_header(response):
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

@app.route('/')
def index():
    return render_template('index.html')

def _distinct_sources():
    data = store._collection.get(include=['metadatas'])
    counts: dict[str, int] = {}
    for m in data.get('metadatas', []):
        src = (m or {}).get('source', 'N/A')
        counts[src] = counts.get(src, 0) + 1
    return counts

def list_documents():
    """
    벡터스토어에 저장된 문서들의 출처와 해당 출처로부터 생성된 청크의 개수를 반환합니다.
    매우 비효율적인 코드. 실제 서비스에서는 벡터스토어에서 메타데이터 집계 기능을 활용하는 것이 좋습니다.
    """
    return [{'source': s, 'chunks': c} for s, c in sorted(_distinct_sources().items())]

@app.get('/files')
def files():
    """
    벡터스토어에 저장된 문서들이 따로 저장되어이 있진 않다. 
    모든 청크 데이터를 다 읽어서 src/chunks 갯수를 세어서 문서로 간주한다.
    """
    return jsonify({'files': list_documents()})

def allowed_file(filename):
    ALLOWED_EXT = {'pdf'}
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXT

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if file and allowed_file(file.filename):
        # 파일이 정상적으로 받아졌으면 지정된 폴더에 저장한다.
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        # 업로드된 파일을 벡터스토어에 저장
        try:
            chunk_count = load_and_store(file_path)
            return jsonify({"message": f"파일이 업로드되었습니다. ({chunk_count}개 청크 저장)"}), 200
        except ValueError as e:
            return jsonify({"message": str(e)}), 400
    return jsonify({"message": "파일 업로드 실패"}), 400

def delete_document(source):
    # 컬렉션에서 메타데이터의 source가 일치하는 문서들을 찾아서 삭제한다.
    store._collection.delete(where={"source": source})

    # 2. DATA 안에 PDF 파일을 보관 중이라면 지운다.
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], source)
    if os.path.exists(file_path):
        os.remove(file_path)
        
    return True

@app.route('/delete/<path:source>', methods=['DELETE'])
def delete(source):
    existed = delete_document(source)
    msg = f"'{source}' 삭제 완료" if existed else f"'{source}' 문서를 찾을 수 없습니다."
    return jsonify({"message": msg, "files": list_documents()}), 200

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        question = data.get('question', "")
        answer = chain.invoke({'question': question})
        return jsonify({"answer": answer}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)