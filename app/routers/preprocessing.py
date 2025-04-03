# app/routers/preprocessing.py
from fastapi import APIRouter
from pydantic import BaseModel
from app.services.preprocessing_service import get_preprocessing_dataset, preprocess_data, get_processed_results, update_label, save_preprocessed_data

class LabelUpdate(BaseModel):
    id: int
    label: int

router = APIRouter()

@router.get("/dataset")
async def get_dataset():
    dataset = get_preprocessing_dataset()
    return dataset

@router.post("/")
async def preprocess():
    processed_data = preprocess_data()
    return {"message": "Preprocessing selesai", "processed_data": processed_data}

@router.get("/results")
async def get_results():
    results = get_processed_results()
    return results

@router.post("/label")
async def update_label_data(label_data: LabelUpdate):
    update_label(label_data)
    return {"message": "Label berhasil diperbarui"}

@router.post("/save")
async def save_data():
    save_preprocessed_data()
    return {"message": "Data berhasil disimpan setelah preprocessing"}