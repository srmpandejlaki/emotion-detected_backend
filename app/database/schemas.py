from pydantic import BaseModel
from typing import Optional, List, Dict
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
class DataCollectionCreate(BaseModel):
    text_data: str
    id_label: Optional[int]  # id label boleh kosong

    class Config:
        orm_mode = True


class DataCollection(BaseModel):
    id_data: int
    text_data: str
    id_label: Optional[int]
    emotion: Optional[EmotionLabelResponse]

    class Config:
        orm_mode = True


class PaginatedDataCollectionResponse(BaseModel):
    total_data: int
    current_page: int
    total_pages: int
    data: List[DataCollection]


# ===== PREPROCESS RESULT =====
class PreprocessingCreate(BaseModel):
    id_data: int


class PreprocessingManyRequest(BaseModel):
    id_data_list: List[int]


class PreprocessingResponse(BaseModel):
    id_process: int
    id_data: int
    data: Optional[DataCollection]
    text_preprocessing: str
    is_processed: bool
    automatic_emotion: Optional[str]
    processed_at: datetime

    class Config:
        orm_mode = True


class PreprocessingUpdate(BaseModel):
    text_preprocessing: Optional[str] = None
    id_label: Optional[str] = None


class PaginatedPreprocessingResponse(BaseModel):
    total_data: int
    current_page: int
    total_pages: int
    preprocessing: List[PreprocessingResponse]


class ProcessingRequest(BaseModel):
    ratio_data: str  # Contoh: "70:30"

class ProcessResultSchema(BaseModel):
    id_process: int
    text_preprocessing: str
    id_data: int
    automatic_emotion: Optional[str]
    processed_at: datetime

    class Config:
        orm_mode = True

class ProcessResultResponse(BaseModel):
    id_process: int
    text_preprocessing: str
    automatic_emotion: Optional[str]
    id_label: int
    emotion_name: str

    class Config:
        orm_mode = True

class EmotionPredictionMetrics(BaseModel):
    label_id: int
    precision: float
    recall: float

class ConfusionMatrixEntry(BaseModel):
    label_id: int
    predicted_label_id: int
    total: int

class ProcessingResponse(BaseModel):
    accuracy: float
    confusion_matrix: List[ConfusionMatrixEntry]
    metrics: List[EmotionPredictionMetrics]

class UpdateManualLabelRequest(BaseModel):
    id: int 
    new_emotion: str


class UpdatePredictedLabelRequest(BaseModel):
    id: int
    new_emotion: str


class TrainResultSchema(BaseModel):
    model_id: int
    accuracy: float
    total_data: int
    ambiguous_count: int
    ratio_used: str

    class Config:
        orm_mode = True
        

# ===== VALIDATION DATA =====
class TestDataResponse(BaseModel):
    id_data: int
    text_preprocessing: str
    automatic_label: Optional[int]

    class Config:
        orm_mode = True

class ValidationDataSchema(BaseModel):
    id_process: int
    is_correct: bool

    class Config:
        orm_mode = True


# ===== VALIDATION RESULT =====
class ValidationResultBase(BaseModel):
    id_process: int
    is_correct: bool


class ValidationResultCreate(ValidationResultBase):
    model_id: int
    accuracy: float
    matrix_id: int
    metrics_id: int
    validation_data: List[ValidationDataSchema]


class ValidationResultResponse(ValidationResultBase):
    id_validation: int
    created_at: Optional[datetime] = None
    validation_data: List[ValidationDataSchema]

    class Config:
        orm_mode = True


# ===== VALIDATION REQUEST & RESPONSE =====
class ValidationSingleInput(BaseModel):
    text: str


class ValidationBatchInput(BaseModel):
    texts: List[str]


class ValidationResponse(BaseModel):
    text: str
    predicted_emotion: str


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
