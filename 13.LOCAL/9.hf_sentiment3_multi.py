# 사전 학습된 BERT 모델과 토크나이저를 로드합니다.
from transformers import BertTokenizer, BertForSequenceClassification
import torch

model_name = 'nlptown/bert-base-multilingual-uncased-sentiment'
tokenizer = BertTokenizer.from_pretrained(model_name)

model = BertForSequenceClassification.from_pretrained(model_name)

text = "이 영화 정말 재미있어요! 강추합니다." # 4
text = "으 별로에요." # 0

inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class = logits.argmax().item()

# 예측된 감정 점수는 0에서 4까지의 정수로, 각각 매우 부정적, 부정적, 중립적, 긍정적, 매우 긍정적을 나타냅니다.
# print(f"예측된 감정 점수: {predicted_class}")

texts = [
    "이 식당 너무 별로에요.",
    "음식이 정말 맛있어요! 강추합니다.",
    "서비스가 최악이었어요. 다시는 안 갈 거예요.",
    "가격이 너무 비싸요. 가성비가 안 좋아요.",
    "친절한 직원과 빠른 서비스에 만족했습니다.",
    "그냥 그런 경험이었어요. 특별히 좋지도 나쁘지도 않았어요.",
]
inputs = tokenizer(texts, return_tensors="pt", truncation=True, padding=True)

with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_classes = logits.argmax().item()
    predictions = torch.argmax(logits, dim=1)

for text, pred in zip(texts, predictions):
    print(f"텍스트: {text}\n예측된 감정 점수: {pred.item()}\n{'-'*50}")