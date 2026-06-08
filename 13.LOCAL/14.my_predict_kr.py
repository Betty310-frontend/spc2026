import os
from transformers import pipeline

MODEL_DIR = "./my_local_model"

classifier = pipeline("sentiment-analysis", model=MODEL_DIR, tokenizer=MODEL_DIR)

test_sentences = [
    "저만의 AI 모델을 쓰는 게 정말 좋아요!",
    "이건 지금까지 최악의 경험이에요.",
    "이건 지금까지 최고의 경험이에요.",
    "기분이 너무 안 좋아요..."
]

for text in test_sentences:
    result = classifier(text)[0]
    print(f"문장: {text}, 결과: {result['label']}, 점수: {result['score']:.4f}")