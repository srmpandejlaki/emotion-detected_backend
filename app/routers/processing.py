from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.processing_service import train_model, load_latest_metrics

router = APIRouter(prefix="/processing", tags=["Processing"])

@router.post("/train", summary="Melatih model Naïve Bayes dengan rasio dataset")
async def train(
    ratio: str = Query(..., description="Format rasio contoh: '80:20'"),
    db: Session = Depends(get_db)
):
    if ":" not in ratio:
        raise HTTPException(status_code=400, detail="Format rasio tidak valid. Gunakan format seperti '80:20'.")

    result, error_message = train_model(ratio, db)
    if error_message:
        raise HTTPException(status_code=400, detail=error_message)

    return {
        "message": "Model berhasil dilatih.",
        "metrics": result["metrics"],
        "test_data": result["test_data"].to_dict()
    }

@router.get("/metrics", summary="Mendapatkan metrik evaluasi model terbaru")
async def get_metrics():
    metrics = load_latest_metrics()
    if not metrics:
        raise HTTPException(status_code=404, detail="Belum ada metrik evaluasi yang tersedia.")
    
    return {
        "message": "Metrik evaluasi terbaru",
        "metrics": metrics
    }
