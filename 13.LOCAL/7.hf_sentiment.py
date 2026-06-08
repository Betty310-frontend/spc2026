"""
분류 (text classification) 
작업을 위한 Hugging Face 모델을 사용하여 감정 분석을 수행하는 예제입니다. 
이 코드는 Hugging Face Hub에서 사전 학습된 모델을 로드하고, 텍스트 데이터를 입력으로 받아 감정 분석 결과를 출력합니다.
"""

# pip install transformers torch
from transformers import pipeline

# distilbert/distilbert-base-uncased-finetuned-sst-2-english 모델을 사용하여 감정 분석 파이프라인을 생성합니다.
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")

# result = sentiment_analyzer("I'm hungry") # [{'label': 'NEGATIVE', 'score': 0.9988470077514648}]
# result = sentiment_analyzer("I love this movie! It's fantastic and heartwarming.") # [{'label': 'POSITIVE', 'score': 0.9998869895935059}]
# result = sentiment_analyzer("I'm tired") # [{'label': 'NEGATIVE', 'score': 0.999774158000946}]
result = sentiment_analyzer(["I'm tired", "I love this movie! It's fantastic and heartwarming."]) # [{'label': 'NEGATIVE', 'score': 0.999774158000946}, {'label': 'POSITIVE', 'score': 0.9998869895935059}]
print(result)