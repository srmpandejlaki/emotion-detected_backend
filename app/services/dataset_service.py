import pandas as pd
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import Dataset
from app.schemas import DatasetCreate
from app.utils.validation_utils import validate_csv_columns
from app.utils.logging_utils import log_error
from app.utils.temp_storage import temp_data, clear_temp_data, add_temp_data, get_temp_data
# (opsional) from app.utils.db_handler import dataset_exists

def process_uploaded_csv(file):
    """Proses file CSV dan menyimpannya sementara untuk preview."""
    try:
        df = pd.read_csv(file)
        validate_csv_columns(df, required_columns={"text"})
        dataset = df.to_dict(orient="records")

        # Simpan sementara
        temp_data.clear()
        temp_data.extend(dataset)

        return dataset
    except Exception as e:
        log_error(f"Error in process_uploaded_csv: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

def add_manual_data(text: str):
    """Tambah data manual ke temp_data."""
    if not text or len(text.strip()) < 3:
        raise HTTPException(status_code=400, detail="Teks terlalu pendek")

    data = {"text": text, "label": None}
    add_temp_data(data)
    return get_temp_data()

def get_paginated_dataset(page: int, db: Session):
    """Ambil dataset dari DB dengan paginasi."""
    limit = 10
    offset = (page - 1) * limit
    return db.query(Dataset).offset(offset).limit(limit).all()

def add_dataset_service(data: DatasetCreate, db: Session):
    """Tambah satu entri dataset ke database."""
    if db.query(Dataset).filter(Dataset.text == data.text).first():
        raise HTTPException(status_code=400, detail="Dataset sudah ada")

    new_entry = Dataset(text=data.text, label_id=data.label_id)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

def get_all_datasets_service(db: Session):
    """Ambil semua dataset dari DB."""
    return db.query(Dataset).all()

def save_dataset(db: Session):
    """Simpan semua data dari `temp_data` ke DB."""
    for item in get_temp_data():
        if not db.query(Dataset).filter(Dataset.text == item["text"]).first():
            new_entry = Dataset(text=item["text"], label=item.get("label"))
            db.add(new_entry)

    db.commit()
    clear_temp_data()
    return {"message": "Dataset berhasil disimpan"}
