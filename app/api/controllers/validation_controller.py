from fastapi import APIRouter, HTTPException, Body
from typing import List, Dict
from app.api.services.validation_service import classify_text, classify_texts

router = APIRouter(prefix="/validation", tags=["Validation"])


@router.post("/classify")
def classify_single_text_controller(data: Dict[str, str] = Body(...)):
    text = data.get("text")
    if not text:
        raise HTTPException(status_code=400, detail="Teks tidak boleh kosong.")

    result = classify_text(text)
    if result == "Model belum tersedia":
        raise HTTPException(status_code=400, detail=result)

    return {"predicted_emotion": result}


@router.post("/classify-dataset")
def classify_dataset_controller(data: Dict[str, List[str]] = Body(...)):
    texts = data.get("text")
    if not texts or not isinstance(texts, list):
        raise HTTPException(status_code=400, detail="Input harus berupa list teks.")

    results = classify_texts(texts)
    if results == "Model belum tersedia":
        raise HTTPException(status_code=400, detail=results)

    return {"results": results}
