# Retrieval Augmented Generation
# 증강 검색 생성

import numpy as np # 숫자(배열/matrix)를 잘 다루는 라이브러리

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small") # OpenAI의 임베딩을 해주는 모델 중 하나 (현재 가장 보편적임)

text = "고양이가 소파 위에서 잔다." # 임베딩을 하고 싶은 텍스트
vector = embeddings.embed_query(text) # 텍스트를 벡터로 변환, 위의 문장으로 하나의 점을 찍는다. 
# print(vector) # 벡터 출력

sentences = [
    "고양이가 소파 위에서 잔다.",
    "강아지가 침대 위에서 잔다.",
    "파이썬은 인기 있는 프로그래밍 언어다."
]

vectors = embeddings.embed_documents(sentences) # 여러 문장을 벡터로 변환, 위의 문장들을 각각 점으로 찍는다. 위 문장 기준으로 점 3개 생성

def cosine_similarity(vec1, vec2): # 코사인 유사도 계산 함수
    vec1, vec2 = np.array(vec1), np.array(vec2) # 벡터를 numpy 배열로 변환
    return float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))) # 코사인 유사도 계산

print("=== 우리의 문장 간 유사도 (1.0 = 완전히 동일) ===")
for i, s1 in enumerate(sentences):
    for j, s2 in enumerate(sentences):
        # if i < j: # 중복 계산 방지
        sim = cosine_similarity(vectors[i], vectors[j]) # 벡터 간 유사도 계산
        print(f" {sim:.4f} {s1[:20]} <-> {s2[:20]}") # 유사도와 문장 일부 출력