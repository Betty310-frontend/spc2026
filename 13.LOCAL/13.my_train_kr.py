"""
나만의 데이터로 모델 추가 학습하기 (fine-tuning)
"""

import numpy as np
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
)

from datasets import Dataset

# 학습 데이터 추가
train_data = {
    "text": [
        "정말 마음에 들어요!",
        "정말 형편없네요.",
        "정말 즐거웠어요.",
        "이건 싫어요.",
        "정말 환상적이에요!",
        "정말 끔찍해요.",
        "정말 만족스럽습니다.",
        "정말 실망스러워요.",
        "최악의 경험이었어요.",
        "최고의 경험이었어요.",
        "완전히 환상적이에요!"
    ],
    "label": [1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1]
}

eval_data = {
    "text": [
        "오늘 기분이 아주 좋아요!",
        "서비스가 정말 나빴어요.",
        "매우 만족합니다.",
        "이건 마음에 들지 않아요.",
        "이건 최고예요!"
    ],
    "label": [1, 0, 1, 0, 1]
}

model_name = "beomi/kcbert-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)

def tokenize(batch):
    return tokenizer(batch['text'], padding="max_length", truncation=True)

train_ds = Dataset.from_dict(train_data).map(tokenize, batched=True)
eval_ds = Dataset.from_dict(eval_data).map(tokenize, batched=True)

model=  AutoModelForSequenceClassification.from_pretrained(
    model_name, 
    num_labels=2, 
    id2label={0: "부정", 1: "긍정"}, 
    label2id={"부정": 0, "긍정": 1}
)

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    
    return {
        "accuracy": float((preds == labels).mean())
    }

args = TrainingArguments(
    output_dir="./results",
    eval_strategy="epoch",
    save_strategy="epoch",
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    num_train_epochs=20,
    logging_steps=1
)

trainer = Trainer(
    model=model, 
    args=args,
    train_dataset=train_ds,
    eval_dataset=eval_ds,
    compute_metrics=compute_metrics
)

trainer.train()
print(f"평가결과: {trainer.evaluate()}")

save_path="./my_local_model"
model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path)
print(f"내 모델 저장 완료: {save_path}")