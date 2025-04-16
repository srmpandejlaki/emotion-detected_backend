import pandas as pd
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.database.model_database import Dataset

# Data sementara sebelum disimpan ke database
temp_data = []

def process_uploaded_csv(file):
    try:
        df = pd.read_csv(file)

        # Pastikan file memiliki kolom "text"
        if "text" not in df.columns:
            raise HTTPException(status_code=400, detail="CSV harus memiliki kolom 'text'")

        # Konversi data ke dictionary
        dataset = df.to_dict(orient="records")

        # Simpan sementara untuk preview
        global temp_data
        temp_data = dataset

        return dataset
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def add_manual_data(text: str):
    if not text or len(text.strip()) < 3:
        raise HTTPException(status_code=400, detail="Teks terlalu pendek")

    data = {"text": text, "label": None}
    temp_data.append(data)
    return temp_data

def get_paginated_dataset(page: int, db: Session):
    limit = 10
    offset = (page - 1) * limit

    dataset = db.query(Dataset).offset(offset).limit(limit).all()

    return dataset

def save_dataset(data: list, db: Session):
    global temp_data

    for item in temp_data:
        if not db.query(Dataset).filter(Dataset.text == item["text"]).first():
            new_entry = Dataset(text=item["text"], label=item.get("label"))
            db.add(new_entry)

    db.commit()
    temp_data = []  # Kosongkan setelah disimpan
    return {"message": "Dataset berhasil disimpan"}
