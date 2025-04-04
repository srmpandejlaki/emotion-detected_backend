from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Body
from app.dependencies import get_db
from app.services import model, validation
from sqlalchemy.orm import Session
import pandas as pd
import io

router = APIRouter(prefix="/evaluation", tags=["Evaluation"])

@router.post("/validate-model")
async def validate_model(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not model.is_model_available():
        raise HTTPException(status_code=404, detail="Model belum tersedia.")

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File harus berupa CSV.")

    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))

        if "text" not in df.columns or "label" not in df.columns:
            raise HTTPException(
                status_code=400,
                detail="File CSV harus memiliki kolom 'text' dan 'label'."
            )

        results = model.evaluate_model_with_csv(df, db)

        return {
            "message": "Evaluasi berhasil.",
            "confusion_matrix": results["confusion_matrix"],
            "metrics": results["metrics"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict-text")
async def predict_text(
    text: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    if not model.is_model_available():
        raise HTTPException(status_code=404, detail="Model belum tersedia.")

    prediction = validation.predict_single_text(text, db)
    return {
        "text": text,
        "predicted_emotion": prediction
    }

@router.post("/predict-batch")
async def predict_batch(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not model.is_model_available():
        raise HTTPException(status_code=404, detail="Model belum tersedia.")

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File harus berupa CSV.")

    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))

        if "text" not in df.columns:
            raise HTTPException(status_code=400, detail="CSV harus memiliki kolom 'text'.")

        result = validation.predict_batch_texts(df, db)

        return {
            "message": "Prediksi batch berhasil.",
            "results": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))@router.post("/predict-text")
async def predict_text(
    text: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    if not model.is_model_available():
        raise HTTPException(status_code=404, detail="Model belum tersedia.")

    prediction = validation.predict_single_text(text, db)
    return {
        "text": text,
        "predicted_emotion": prediction
    }

@router.post("/predict-batch")
async def predict_batch(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not model.is_model_available():
        raise HTTPException(status_code=404, detail="Model belum tersedia.")

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File harus berupa CSV.")

    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))

        if "text" not in df.columns:
            raise HTTPException(status_code=400, detail="CSV harus memiliki kolom 'text'.")

        result = validation.predict_batch_texts(df, db)

        return {
            "message": "Prediksi batch berhasil.",
            "results": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))