from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class InputData(BaseModel):
    text: str
    label: Optional[str] = None

# lama

class DatasetBase(BaseModel):
    text: str
    label_id: Optional[int] = None

class DatasetCreate(DatasetBase):  
    label_id: int  

class DatasetResponse(DatasetBase):
    id: int
    model_config = ConfigDict(from_attributes=True)  # Untuk Pydantic v2

class ValidationResultBase(BaseModel):
    text: str
    label_id: int
    accuracy: float  
    precision: float
    recall: float

class ValidationResultResponse(ValidationResultBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
