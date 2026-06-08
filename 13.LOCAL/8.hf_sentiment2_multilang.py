"""
분류 (text classification) 
작업을 위한 Hugging Face 모델을 사용하여 감정 분석을 수행하는 예제입니다. 
이 코드는 Hugging Face Hub에서 사전 학습된 모델을 로드하고, 텍스트 데이터를 입력으로 받아 감정 분석 결과를 출력합니다.
"""

# pip install transformers torch
from transformers import pipeline

# tabularisai/multilingual-sentiment-analysis 모델을 사용하여 감정 분석 파이프라인을 생성합니다.
MODEL_NAME = "tabularisai/multilingual-sentiment-analysis"
sentiment_analyzer = pipeline("text-classification", model=MODEL_NAME)

result = sentiment_analyzer(["I'm tired", "I love this movie! It's fantastic and heartwarming."]) # [{'label': 'Negative', 'score': 0.6209602355957031}, {'label': 'Very Positive', 'score': 0.5476697087287903}]
# print(result)

comments = [
    "배송이 너무 느려요. 언제 오나요?",
    "품질이 별로예요. 실망했어요.",
    "가격이 너무 비싸요. 가성비가 안 좋아요.",
    "상품이 설명과 달라요. 환불 요청할게요.",
    "상품이 마음에 들지 않아요. 교환하고 싶어요.",

    "상품이 마음에 들어요! 정말 좋아요.",
    "친절한 고객 서비스에 감사드립니다. 정말 만족해요!",
    "배송이 빠르고 상품도 좋아요. 만족합니다.",
    "가격이 적당하고 품질도 좋아요. 추천합니다!",
]

for comment in comments:
    result = sentiment_analyzer(comment)
    print(f"Comment: {comment}\nSentiment: {result}\n")
    print("-" * 50)