from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import (
    CharacterTextSplitter, 
    RecursiveCharacterTextSplitter # 더 똑똑한 텍스트 분할기. 문장 단위로 최대한 분할하려고 시도함
)

loader = TextLoader('./docs/HBM.txt', encoding='utf-8')
documents = loader.load()

doc = documents[0].page_content.strip() # 페이지 내용 양쪽 공백 제거
print(f"원본 글자수: {len(doc)}")

# 일반적으로 1000:200 / 1500:300 / 2000:500 정도로 실제 잘린 내용을 보고 판단함
char_splitter = CharacterTextSplitter(
    separator='\n\n', # 문단 구분자로 줄바꿈 2개 사용
    chunk_size=500, # 위 조각이 작으면, 최대 500자가 될 때까지 합침
    chunk_overlap=100 # 분할된 텍스트 간에 100자씩 겹치도록 설정
)

chunk_char = char_splitter.split_documents(documents)
print(f"[CharSplitter] {len(chunk_char)} 개의 청크로 분할됨")
print(f"첫 번째 청크 글자수: {len(chunk_char[0].page_content)}")

# RecursiveCharacterTextSplitter는 CharacterTextSplitter보다 더 똑똑하게 텍스트를 분할한다.
recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunk_recur = recursive_splitter.split_documents(documents)
print("-" * 50)
print(f"[RecursiveCharacterTextSplitter] {len(chunk_recur)} 개의 청크로 분할됨")
print(f"첫 번째 청크 글자수: {len(chunk_recur[0].page_content)}")