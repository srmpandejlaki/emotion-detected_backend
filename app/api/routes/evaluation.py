from fastapi import APIRouter, UploadFile, File, Depends
import pandas as pd
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.evaluation_service import evaluate_model_with_csv

router = APIRouter()

@router.post("/evaluate", summary="Evaluasi model dengan file CSV data uji")
async def evaluate_model(file: UploadFile = File(...), db: Session = Depends(get_db)):
    df = pd.read_csv(file.file)
    result = evaluate_model_with_csv(df, db)
    return result
