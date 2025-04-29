from fastapi import APIRouter
from typing import List
from app.api.controllers.processing_controller import ProcessingController
from app.database.schemas import (
    ProcessingRequest,
    ProcessingResponse,
    SaveRequest,
    SaveAllRequest
)

router = APIRouter(
    prefix="/processing",
    tags=["Processing"],
)

@router.post("/classify", response_model=List[ProcessingResponse])
def classify_texts(request: ProcessingRequest):
    return ProcessingController.classify_texts(request)

@router.get("/all", response_model=List[ProcessingResponse])
def get_all():
    return ProcessingController.get_all()

@router.get("/{id_process}", response_model=ProcessingResponse)
def get_by_id(id_process: int):
    return ProcessingController.get_by_id(id_process)

@router.delete("/all")
def delete_all():
    ProcessingController.delete_all()
    return {"message": "All records deleted successfully"}

@router.delete("/{id_process}")
def delete_by_id(id_process: int):
    ProcessingController.delete_by_id(id_process)
    return {"message": f"Record with id {id_process} deleted successfully"}

@router.put("/save")
def save_by_id(request: SaveRequest):
    ProcessingController.save_by_id(request)
    return {"message": "Record updated successfully"}

@router.put("/save_all")
def save_all(request: SaveAllRequest):
    ProcessingController.save_all(request)
    return {"message": "All records updated successfully"}
