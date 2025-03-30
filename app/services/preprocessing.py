from sqlalchemy.orm import Session
from app import models
import re

def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Hapus karakter non-huruf
    return text.lower().strip()

def process_all(db: Session):
    data = db.query(models.Dataset).all()
    for row in data:
        row.text = clean_text(row.text)
    db.commit()
    return [{"id": row.id, "text": row.text, "label": row.label} for row in data]
