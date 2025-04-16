import pandas as pd
from sqlalchemy.orm import Session
from app.models import Dataset
from fastapi import HTTPException
from app.schemas import DatasetCreate

# Gunakan list dictionary untuk menyimpan sementara
temp_data = []

def validate_csv_columns(df: pd.DataFrame):
    """Memeriksa apakah CSV memiliki kolom yang sesuai."""
    required_columns = {"text"}
    if not required_columns.issubset(set(df.columns)):
        raise HTTPException(status_code=400, detail=f"CSV harus memiliki kolom {required_columns}")

def process_uploaded_csv(file):
    """Proses file CSV yang diunggah dan menyimpannya untuk preview."""
    try:
        df = pd.read_csv(file)

        # Validasi kolom
        validate_csv_columns(df)

        dataset = df.to_dict(orient="records")

        global temp_data
        temp_data = dataset

        return dataset
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def add_manual_data(text: str):
    """Menambahkan data secara manual ke daftar sementara."""
    if not text or len(text.strip()) < 3:
        raise HTTPException(status_code=400, detail="Teks terlalu pendek")

    data = {"text": text, "label": None}
    temp_data.append(data)
    return temp_data

def get_paginated_dataset(page: int, db: Session):
    """Mengambil dataset dengan paginasi."""
    limit = 10
    offset = (page - 1) * limit

    dataset = db.query(Dataset).offset(offset).limit(limit).all()
    return dataset

def add_dataset_service(data: DatasetCreate, db: Session):
    """Menambahkan dataset ke database."""
    if db.query(Dataset).filter(Dataset.text == data.text).first():
        raise HTTPException(status_code=400, detail="Dataset sudah ada")

    new_entry = Dataset(text=data.text, label_id=data.label_id)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return new_entry

def get_all_datasets_service(db: Session):
    """Mengambil semua dataset dari database."""
    return db.query(Dataset).all()

def save_dataset(db: Session):
    """Menyimpan data dari temp_data ke database."""
    global temp_data

    for item in temp_data:
        if not db.query(Dataset).filter(Dataset.text == item["text"]).first():
            new_entry = Dataset(text=item["text"], label=item.get("label"))
            db.add(new_entry)

    db.commit()
    temp_data = []  # Kosongkan setelah disimpan
    return {"message": "Dataset berhasil disimpan"}