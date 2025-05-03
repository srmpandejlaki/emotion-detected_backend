from pydantic import BaseModel
from typing import Optional, List, Dict, Union
from datetime import datetime


# ===== EMOTION LABEL =====
class EmotionLabelBase(BaseModel):
    emotion_name: str

class EmotionLabelCreate(EmotionLabelBase):
    pass

class EmotionLabelResponse(EmotionLabelBase):
    id_label: int

    class Config:
        orm_mode = True


# ===== DATA COLLECTION =====
class DataCollectionBase(BaseModel):
    text_data: str
    id_label: Optional[int] = None

class DataCollectionCreate(DataCollectionBase):
    pass

class DataCollectionResponse(DataCollectionBase):
    id_data: int
    emotion: Optional[EmotionLabelResponse]

    class Config:
        orm_mode = True


# ===== PROCESS RESULT =====
# Base schema (untuk input data baru ke database) - preprocessing
class ProcessResultBase(BaseModel):
    id_data: int
    text_preprocessing: str
    isProcessed_data: Optional[bool] = False  # default False

# Schema untuk pembuatan data baru (request body dari client)
class ProcessResultCreate(ProcessResultBase):
    pass

# Schema untuk response dari backend (output ke client)
class ProcessResultResponse(ProcessResultBase):
    id_process: int

    class Config:
        orm_mode = True


# ini masuk bagian processing
class ProcessInput(BaseModel):
    texts: List[str]
    labels: List[str]
    id_process_list: List[int]

class ProcessSaveInput(BaseModel):
    id_process: int
    automatic_emotion: Optional[str]

class ProcessSaveManyInput(BaseModel):
    items: List[Dict[str, Union[int, Optional[str]]]]

class ProcessResultSchema(BaseModel):
    id_process: int
    id_data: int
    text_preprocessing: str
    automatic_emotion: Optional[str]

    class Config:
        orm_mode = True

class ProcessingRequest(BaseModel):
    texts: List[str]
    labels: List[str]
    id_process_list: List[int]

class ProcessResultResponse(ProcessResultBase):
    id_process: int
    data: Optional[DataCollectionResponse]  # ← Tambahkan ini untuk akses ke data → emotion

    class Config:
        orm_mode = True

class SaveRequest(BaseModel):
    id_process: int
    automatic_emotion: Optional[str]

class SaveAllRequest(BaseModel):
    data: List[SaveRequest]


# ===== MODEL =====
class ModelBase(BaseModel):
    ratio_data: str
    accuracy: Optional[float] = None
    matrix_id: Optional[int] = None
    metrics_id: Optional[int] = None

class ModelCreate(ModelBase):
    pass

class ModelResponse(ModelBase):
    id_model: int

    class Config:
        orm_mode = True


# ===== MODEL DATA =====
class ModelDataBase(BaseModel):
    id_model: int
    id_process: int

class ModelDataCreate(ModelDataBase):
    pass

class ModelDataResponse(ModelDataBase):
    model: Optional[ModelResponse]
    process_result: Optional[ProcessResultResponse]

    class Config:
        orm_mode = True


# === VALIDATION DATA ===
class ValidationDataSchema(BaseModel):
    id_process: int
    is_correct: bool

    class Config:
        orm_mode = True


# === VALIDATION RESULT ===
class ValidationResultBase(BaseModel):
    model_id: int
    accuracy: float
    matrix_id: int
    metrics_id: int

class ValidationResultCreate(ValidationResultBase):
    validation_data: List[ValidationDataSchema]

class ValidationResultResponse(ValidationResultBase):
    id_validation: int
    created_at: Optional[datetime] = None
    validation_data: List[ValidationDataSchema]

    class Config:
        orm_mode = True


# ===== CONFUSION MATRIX =====
class ConfusionMatrixBase(BaseModel):
    matrix_id: int
    label_id: int
    predicted_label_id: int
    total: int

class ConfusionMatrixCreate(ConfusionMatrixBase):
    pass

class ConfusionMatrixResponse(ConfusionMatrixBase):
    class Config:
        orm_mode = True


# ===== CLASS METRICS =====
class ClassMetricsBase(BaseModel):
    metrics_id: int
    label_id: int
    precision: Optional[float] = None
    recall: Optional[float] = None

class ClassMetricsCreate(ClassMetricsBase):
    pass

class ClassMetricsResponse(ClassMetricsBase):
    class Config:
        orm_mode = True
