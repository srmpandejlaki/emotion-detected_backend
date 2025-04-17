from collections import defaultdict
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Load model sekali saja
MODEL_NAME = "indobenchmark/indobert-base-p1"  # Ganti sesuai model kamu
bert_model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
bert_model.eval()

# Contoh lexicon
# Format: {"word": ["emotion1", "emotion2"]}
emotion_lexicon = {
    "senang": ["joy"],
    "percaya": ["trust"],
    "terkejut": ["shock"],
    "netral": ["netral"],
    "takut": ["fear"],
    "sedih": ["sadness"],
    "marah": ["anger"]
    # Tambahkan lebih banyak kata sesuai kamusmu
}

def predict_with_bert(text: str, label_list: list[str]) -> list[float]:
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = bert_model(**inputs)
        probs = F.softmax(outputs.logits, dim=1).squeeze().tolist()
    return probs  # Sesuaikan urutan dengan label_list

def lexicon_score(text: str, label_list: list[str]) -> dict:
    scores = defaultdict(int)
    words = text.lower().split()
    for word in words:
        if word in emotion_lexicon:
            for emotion in emotion_lexicon[word]:
                scores[emotion] += 1
    total = sum(scores.values()) or 1
    normalized = {k: v / total for k, v in scores.items()}
    return {label: normalized.get(label, 0) for label in label_list}

def combined_score(text: str, label_list: list[str]) -> str:
    bert_probs = predict_with_bert(text, label_list)
    lexicon_probs_dict = lexicon_score(text, label_list)
    lexicon_probs = [lexicon_probs_dict[label] for label in label_list]

    combined = [(b + l) / 2 for b, l in zip(bert_probs, lexicon_probs)]
    best_idx = combined.index(max(combined))
    return label_list[best_idx]
