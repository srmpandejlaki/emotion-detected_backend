from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.config import get_db
from app.api.services.processing_service import ProcessingService
from app.database.schemas import (
    ProcessingRequest,
    ProcessingResponse,
    SaveRequest,
    SaveAllRequest
)

class ProcessingController:
    @staticmethod
    def classify_texts(
        request: ProcessingRequest,
        db: Session = Depends(get_db)
    ) -> List[ProcessingResponse]:
        results = ProcessingService.process_texts(
            db=db,
            texts=request.texts,
            labels=request.labels,
            id_process_list=request.id_process_list
        )
        return [ProcessingResponse(**result) for result in results]

    @staticmethod
    def get_all(db: Session = Depends(get_db)) -> List[ProcessingResponse]:
        records = ProcessingService.get_all(db)
        return [ProcessingResponse(
            id_process=rec.id_process,
            text=rec.text,
            probabilities={},  # Probabilities tidak diambil dari database
            predicted_emotion=rec.automatic_emotion
        ) for rec in records]

    @staticmethod
    def get_by_id(id_process: int, db: Session = Depends(get_db)) -> ProcessingResponse:
        record = ProcessingService.get_by_id(db, id_process)
        if not record:
            raise Exception(f"Data with id {id_process} not found")
        return ProcessingResponse(
            id_process=record.id_process,
            text=record.text,
            probabilities={},  # Probabilities tidak diambil dari database
            predicted_emotion=record.automatic_emotion
        )

    @staticmethod
    def delete_all(db: Session = Depends(get_db)):
        ProcessingService.delete_all(db)

    @staticmethod
    def delete_by_id(id_process: int, db: Session = Depends(get_db)):
        ProcessingService.delete_by_id(db, id_process)

    @staticmethod
    def save_by_id(request: SaveRequest, db: Session = Depends(get_db)):
        ProcessingService.save_by_id(
            db=db,
            id_process=request.id_process,
            automatic_emotion=request.automatic_emotion
        )

    @staticmethod
    def save_all(request: SaveAllRequest, db: Session = Depends(get_db)):
        data = [item.dict() for item in request.data]
        ProcessingService.save_all(db, data)
