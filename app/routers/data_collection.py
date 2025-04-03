from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.data_service import (
    process_uploaded_file, 
    add_manual_data, 
    get_paginated_dataset, 
    save_dataset
)

router = APIRouter(
    prefix="/data-collection",
    tags=["Data Collection"]
)

# Endpoint untuk upload CSV (data belum masuk database, hanya ditampilkan di frontend)
@router.post("/upload-csv")
def upload_csv(file: UploadFile = File(...)):
    try:
        # Proses file CSV menjadi preview data
        dataset = process_uploaded_file(file)
        return {"message": "File processed successfully", "data": dataset}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint untuk menambahkan data manual
@router.post("/add-data")
def add_data(text: str):
    try:
        # Menambahkan data manual ke list sementara
        data = add_manual_data(text)
        return {"message": "Data added successfully", "data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint untuk menampilkan dataset dengan pagination
@router.get("/dataset")
def get_dataset(page: int = 1, db: Session = Depends(get_db)):
    try:
        # Mengambil data dari database dengan pagination
        dataset = get_paginated_dataset(page, db)
        return {"message": "Dataset retrieved", "data": dataset}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint untuk menyimpan dataset ke database
@router.post("/save-dataset")
def save_dataset_api(data: list, db: Session = Depends(get_db)):
    try:
        # Menyimpan data yang sudah diproses ke dalam database
        saved_data = save_dataset(data, db)
        return {"message": "Dataset saved successfully", "data": saved_data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
