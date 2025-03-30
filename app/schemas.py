from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_admin: bool

    class Config:
        from_attributes = True

class EmotionLabelBase(BaseModel):
    name: str

class EmotionLabelResponse(EmotionLabelBase):
    id: int
    
    class Config:
        from_attributes = True

class DatasetBase(BaseModel):
    text: str
    label_id: Optional[int] = None

class DatasetResponse(DatasetBase):
    id: int

    class Config:
        from_attributes = True

class ValidationResultBase(BaseModel):
    text: str
    label_id: int
    accuracy: int
    precision: int
    recall: int

class ValidationResultResponse(ValidationResultBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True