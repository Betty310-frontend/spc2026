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
        "I love this!",
        "This is terrible.",
        "I really enjoyed it.",
        "I hate this.",
        "This is fantastic!",
        "This is awful.",
        "I am so happy with this.",
        "I am very disappointed.",
        "Worst experience ever.",
        "Best experience ever.",
        "Absolutely fantastic!"
    ],
    "label": [1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1] # 긍정: 1, 부정: 0
}

eval_data = {
    "text": [
        "I feel great today!",
        "The service was bad.",
        "I am very satisfied.",
        "I am not happy with this.",
        "This is the best!"
    ],
    "label": [1, 0, 1, 0, 1]
}

model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)

def tokenize(batch):
    return tokenizer(batch['text'], padding="max_length", truncation=True)

train_ds = Dataset.from_dict(train_data).map(tokenize, batched=True)
eval_ds = Dataset.from_dict(eval_data).map(tokenize, batched=True)

model=  AutoModelForSequenceClassification.from_pretrained(
    model_name, 
    num_labels=2, 
    id2label={0: "NEGATIVE", 1: "POSITIVE"}, 
    label2id={"NEGATIVE": 0, "POSITIVE": 1}
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
    num_train_epochs=3,
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