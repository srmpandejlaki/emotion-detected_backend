from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.api.controllers import validation_controller
from app.database.schemas import ValidationResultResponse

router = APIRouter(
    prefix="/validation",
    tags=["Validation"]
)

@router.get("/", response_model=List[ValidationResultResponse])
def get_all_validation_results(db: Session = Depends(get_db)):
    """
    Mengambil semua hasil validasi yang pernah dilakukan.
    """
    return validation_controller.get_all_validation_results(db)


@router.get("/{validation_id}", response_model=ValidationResultResponse)
def get_validation_by_id(validation_id: int, db: Session = Depends(get_db)):
    """
    Mengambil hasil validasi berdasarkan ID.
    """
    result = validation_controller.get_validation_result_by_id(validation_id, db)
    if not result:
        raise HTTPException(status_code=404, detail="Validation result not found")
    return result


@router.post("/csv", response_model=ValidationResultResponse)
async def validate_from_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Mengunggah file CSV untuk melakukan validasi manual terhadap model.
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    try:
        result = await validation_controller.validate_from_csv(file, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
