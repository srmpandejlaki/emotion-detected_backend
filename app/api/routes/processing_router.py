from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api.services.processing_service import ProcessingService
from app.database.config import get_db
from app.database.schemas import ProcessInput, ProcessSaveInput, ProcessSaveManyInput, ProcessResultSchema

router = APIRouter(prefix="/processing", tags=["Processing"])

@router.get("/list", response_model=List[ProcessResultSchema])
def get_all_processing(db: Session = Depends(get_db)):
    return ProcessingService.get_all(db)

@router.get("/{id_process}", response_model=ProcessResultSchema)
def get_processing_by_id(id_process: int, db: Session = Depends(get_db)):
    result = ProcessingService.get_by_id(db, id_process)
    if not result:
        raise HTTPException(status_code=404, detail="Process not found")
    return result

@router.delete("/list", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_processing(db: Session = Depends(get_db)):
    ProcessingService.delete_all(db)
    return

@router.delete("/{id_process}", status_code=status.HTTP_204_NO_CONTENT)
def delete_processing_by_id(id_process: int, db: Session = Depends(get_db)):
    ProcessingService.delete_by_id(db, id_process)
    return

@router.post("/process-texts")
def process_texts(data: ProcessInput, db: Session = Depends(get_db)):
    try:
        result = ProcessingService.process_texts(
            db=db,
            texts=data.texts,
            labels=data.labels,
            id_process_list=data.id_process_list
        )
        return {"status": "success", "result": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/save")
def save_processing_result(data: ProcessSaveInput, db: Session = Depends(get_db)):
    result = ProcessingService.save_by_id(
        db=db,
        id_process=data.id_process,
        automatic_emotion=data.automatic_emotion
    )
    return result

@router.put("/save-all")
def save_all_processing_results(data: ProcessSaveManyInput, db: Session = Depends(get_db)):
    result = ProcessingService.save_all(db=db, data=data.items)
    return result
