from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
# MNLI (Multi-Genre Natural Language Inference) 모델을 사용하여 제로샷 분류를 수행하는 파이프라인을 생성합니다.
"""
내부적으로는 문장/문장 연관성
  1. 함의 (Entailment)
  - ex) 오늘 비가 많이 내린다. -> 우산이 필요할 수 있다
  2. 모순 (Contradiction)
  - ex) 오늘 비가 많이 내린다. -> 오늘은 맑은 날이다.
  3. 중립 (Neutral)
  - ex) 오늘 비가 많이 내린다. -> 나는 피자를 좋아한다.
"""

text = "I just upgraded my computer's graphics card"
# 나는 내 컴퓨터의 그래픽 카드를 업그레이드했다.
# -> 이 문장은 기술에 관한 것이다.
# -> 이 문장은 스포츠에 관한 것이다.
# -> 이 문장은 요리에 관한 것이다.
# -> 이 문장은 정치에 관한 것이다.

candidate_labels = ["technology", "sports", "cooking", "politics"]

result = classifier(text, candidate_labels)
print(f"입력 텍스트: {text}")
for label, score in zip(result['labels'], result['scores']):
    print(f"라벨: {label}, 점수: {score:.4f}")

print(f"최종 분류: {result['labels'][0]}")