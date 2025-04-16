from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Body
from sqlalchemy.orm import Session
import pandas as pd
import io

from database.database import get_db
from services.model_service import is_model_available, evaluate_model_with_csv
from services.validation_service import predict_single_text, predict_batch_texts

router = APIRouter(prefix="/validation", tags=["Validation"])

@router.post("/evaluate", summary="Evaluasi model dengan file CSV data uji")
async def validate_model(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not is_model_available():
        raise HTTPException(status_code=404, detail="Model belum tersedia.")

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File harus berupa CSV.")

    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))

        # Validasi kolom
        if "text" not in df.columns or "label" not in df.columns:
            raise HTTPException(status_code=400, detail="CSV harus memiliki kolom 'text' dan 'label'.")

        df = df.dropna(subset=["text"])  # Hapus baris dengan teks kosong

        results = evaluate_model_with_csv(df, db)

        return {
            "message": "Evaluasi berhasil.",
            "confusion_matrix": results["confusion_matrix"],
            "metrics": results["metrics"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict-single", summary="Prediksi emosi dari input tunggal")
async def predict_text(text: str = Body(..., embed=True), db: Session = Depends(get_db)):
    if not is_model_available():
        raise HTTPException(status_code=404, detail="Model belum tersedia.")

    prediction = predict_single_text(text, db)
    return {
        "text": text,
        "predicted_emotion": prediction
    }

@router.post("/predict-batch", summary="Prediksi emosi dari file CSV")
async def predict_batch(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not is_model_available():
        raise HTTPException(status_code=404, detail="Model belum tersedia.")

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File harus berupa CSV.")

    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))

        # Validasi kolom
        if "text" not in df.columns:
            raise HTTPException(status_code=400, detail="CSV harus memiliki kolom 'text'.")

        df = df.dropna(subset=["text"])  # Hapus baris kosong

        result = predict_batch_texts(df, db)

        return {
            "message": "Prediksi batch berhasil.",
            "results": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
