from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.api.services import validation_service
from app.database.config import get_db
from app.database.schemas import ValidationResultCreate

router = APIRouter(
    prefix="/validation",
    tags=["Validation"]
)

@router.post("/run")
def validate_model(payload: ValidationResultCreate, db: Session = Depends(get_db)):
    try:
        result = validation_service.perform_validation(payload, db)
        return {"message": "Validation completed successfully", "result": result}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
def get_all_results(db: Session = Depends(get_db)):
    try:
        results = validation_service.get_all_validation_results(db)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{validation_id}")
def get_validation_by_id(validation_id: int, db: Session = Depends(get_db)):
    try:
        result = validation_service.get_validation_result_by_id(validation_id, db)
        if not result:
            raise HTTPException(status_code=404, detail="Validation result not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete-all")
def delete_all_results(db: Session = Depends(get_db)):
    try:
        validation_service.delete_all_validation_results(db)
        return {"message": "All validation data has been deleted successfully"}
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
