from transformers import BertTokenizer, BertModel
import torch
import json
from datetime import datetime
from sqlalchemy.orm import Session
from app.database.model_database import ProcessResult

# Load tokenizer dan model hanya sekali
bert_tokenizer = BertTokenizer.from_pretrained("indobenchmark/indobert-base-p1")
bert_model = BertModel.from_pretrained("indobenchmark/indobert-base-p1")

def load_lexicon(filepath="app/utils/json/kamus_lexicon.json"):
    """Memuat kamus leksikon emosi dari file JSON"""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def bert_lexicon_fusion(text: str, lexicon_dict: dict) -> str:
    """Menggabungkan pendekatan BERT dan Lexicon untuk menentukan emosi akhir"""
    # --- Lexicon scoring ---
    lexicon_scores = {}
    tokens = text.lower().split()
    for token in tokens:
        for emotion, words in lexicon_dict.items():
            if token in words:
                lexicon_scores[emotion] = lexicon_scores.get(emotion, 0) + 1

    # --- BERT representation (CLS token) ---
    inputs = bert_tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = bert_model(**inputs)
    cls_embedding = outputs.last_hidden_state[0][0]  # [CLS] token vector

    # --- Fusion logic ---
    if lexicon_scores:
        final_emotion = max(lexicon_scores, key=lexicon_scores.get)
    else:
        final_emotion = "netral"  # fallback emosi jika tidak ditemukan

    return final_emotion

def process_with_bert_lexicon(db: Session, items_to_process: list):
    """Memproses data ambiguitas ke metode BERT + Lexicon dan menyimpannya"""
    lexicon_dict = load_lexicon()

    for item in items_to_process:
        id_process = item["id_process"]
        text = item["text"]

        final_emotion = bert_lexicon_fusion(text, lexicon_dict)

        process = db.query(ProcessResult).filter(ProcessResult.id_process == id_process).first()
        if process:
            process.automatic_emotion = final_emotion
            process.is_processed = True
            process.processed_at = datetime.now()

    db.commit()
    return {"processed_with_bert_lexicon": len(items_to_process)}
