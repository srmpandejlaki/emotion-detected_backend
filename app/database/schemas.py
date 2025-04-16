from pydantic import BaseModel
from typing import Optional, List


# ---------- Label Emotion ----------
class LabelEmotionBase(BaseModel):
    nama_label: str

class LabelEmotionCreate(LabelEmotionBase):
    pass

class LabelEmotion(LabelEmotionBase):
    id_label: int

    class Config:
        orm_mode = True


# ---------- Data Collection ----------
class DataCollectionBase(BaseModel):
    text_data: str
    label_id: Optional[int]

class DataCollectionCreate(DataCollectionBase):
    pass

class DataCollection(DataCollectionBase):
    id_data: int

    class Config:
        orm_mode = True


# ---------- Process Result ----------
class ProcessResultBase(BaseModel):
    id_data: int
    text_preprocessing: str
    is_training_data: bool
    automatic_label: Optional[int]

class ProcessResultCreate(ProcessResultBase):
    pass

class ProcessResult(ProcessResultBase):
    id_process: int

    class Config:
        orm_mode = True


# ---------- Model ----------
class ModelBase(BaseModel):
    ratio_data: str
    accuracy: Optional[float]
    matrix_id: Optional[int]
    metrics_id: Optional[int]

class ModelCreate(ModelBase):
    pass

class Model(ModelBase):
    id_model: int

    class Config:
        orm_mode = True


# ---------- Model Data ----------
class ModelDataBase(BaseModel):
    id_model: int
    id_process: int

class ModelDataCreate(ModelDataBase):
    pass

class ModelData(ModelDataBase):
    class Config:
        orm_mode = True


# ---------- Validation Result ----------
class ValidationResultBase(BaseModel):
    model_id: int
    accuracy: Optional[float]
    matrix_id: Optional[int]
    metrics_id: Optional[int]

class ValidationResultCreate(ValidationResultBase):
    pass

class ValidationResult(ValidationResultBase):
    id_validation: int

    class Config:
        orm_mode = True


# ---------- Validation Data ----------
class ValidationDataBase(BaseModel):
    id_validation: int
    id_process: int
    is_correct: bool

class ValidationDataCreate(ValidationDataBase):
    pass

class ValidationData(ValidationDataBase):
    class Config:
        orm_mode = True


# ---------- Confusion Matrix ----------
class ConfusionMatrixBase(BaseModel):
    matrix_id: int
    label_id: int
    predicted_label_id: int
    total: int

class ConfusionMatrixCreate(ConfusionMatrixBase):
    pass

class ConfusionMatrix(ConfusionMatrixBase):
    class Config:
        orm_mode = True


# ---------- Class Metrics ----------
class ClassMetricsBase(BaseModel):
    metrics_id: int
    label_id: int
    precision: Optional[float]
    recall: Optional[float]

class ClassMetricsCreate(ClassMetricsBase):
    pass

class ClassMetrics(ClassMetricsBase):
    class Config:
        orm_mode = True
