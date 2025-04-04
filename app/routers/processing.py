from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from app.services import model_service
from app.dependencies import get_db

router = APIRouter(prefix="/processing", tags=["Processing"])

@router.post("/train")
def train_model(
    ratio: str = Query("80:20", description="Rasio pembagian data latih:uji, contoh: 80:20"),
    db: Session = Depends(get_db)
):
    try:
        result, error = model_service.train_model(ratio, db)
        if error:
            raise HTTPException(status_code=400, detail=error)

        # Simpan file data uji
        file_path = model_service.save_test_data_to_csv(result["test_data"])
        return {
            "message": "Model berhasil dilatih.",
            "metrics": result["metrics"],
            "download_test_data": f"/processing/download-test-data"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metrics")
def get_model_metrics():
    if not model_service.is_model_available():
        raise HTTPException(status_code=404, detail="Model belum tersedia.")

    metrics = model_service.load_latest_metrics()
    return {"metrics": metrics}


@router.get("/download-test-data")
def download_test_data():
    file_path = model_service.TEST_DATA_PATH
    return FileResponse(path=file_path, filename="data_uji.csv", media_type="text/csv")
