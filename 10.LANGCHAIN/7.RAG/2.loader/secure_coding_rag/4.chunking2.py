# pip install pypdf
# 이 외에도 다양한 PDF 로더가 있음. fitz 도 유명

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = PyPDFLoader('./docs/Javascript_secure_coding.pdf')
pages = loader.load()

print(f"PDF 페이지 수: {len(pages)}\n")

for p in pages:
    if p.page_content.strip(): # 페이지 내용이 비어있지 않은 경우에만 출력
        print(f"metadata: {p.metadata}\n")
        print(f"page_content (앞 100자):\n{p.page_content[:100]}...\n")
        break # 첫 번째 페이지 내용만 출력하도록 설정

splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=500
)

chunks = splitter.split_documents(pages)
print(f"청킹 후 문서 갯수: {len(chunks)}\n")

first_chunk = chunks[0]
print(first_chunk.metadata)
print(first_chunk.page_content)
print(f"\n{'-' * 50}\n")

nth_chunk = chunks[100]
print(nth_chunk.metadata)
print(nth_chunk.page_content)