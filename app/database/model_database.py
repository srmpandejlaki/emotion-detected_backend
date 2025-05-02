from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, UniqueConstraint, DateTime, Text
from sqlalchemy.orm import relationship, declarative_base
from app.database.config import Base

Base = declarative_base()

# ===== EMOTION LABEL =====
class EmotionLabel(Base):
    __tablename__ = 'emotion_label'

    id_label = Column(Integer, primary_key=True, index=True)
    emotion_name = Column(String(50), unique=True, nullable=False)

    # Relasi dengan DataCollection
    data = relationship("DataCollection", back_populates="emotion")


# ===== DATA COLLECTION =====
class DataCollection(Base):
    __tablename__ = 'data_collection'

    id_data = Column(Integer, primary_key=True, index=True)
    text_data = Column(Text, nullable=False)
    id_label = Column(Integer, ForeignKey('emotion_label.id_label'), nullable=True)

    # Kolom hasil preprocessing
    preprocessing_result = Column(Text, nullable=True)

    # Relasi ke label
    emotion = relationship("EmotionLabel", back_populates="data")

    # Relasi ke hasil preprocessing
    preprocessing = relationship("ProcessResult", back_populates="data", uselist=False)


# ===== PROCESS RESULT (PREPROCESSING) =====
class ProcessResult(Base):
    __tablename__ = 'process_result'

    id_process = Column(Integer, primary_key=True, index=True)
    id_data = Column(Integer, ForeignKey('data_collection.id_data'), nullable=False)
    text_preprocessing = Column(Text, nullable=False)

    # Relasi balik ke data_collection
    data = relationship("DataCollection", back_populates="preprocessing")

# Model: Stores information about the model and its evaluation.
class Model(Base):
    __tablename__ = "model"
    id_model = Column(Integer, primary_key=True, index=True)
    ratio_data = Column(String(10), nullable=False)
    accuracy = Column(Float)
    matrix_id = Column(Integer)
    metrics_id = Column(Integer)

    model_data = relationship("ModelData", back_populates="model")
    validation_results = relationship("ValidationResult", back_populates="model")

# Model Data: Stores the mapping of the model with the processed data used for training.
class ModelData(Base):
    __tablename__ = "model_data"
    id_model = Column(Integer, ForeignKey("model.id_model"), primary_key=True)
    id_process = Column(Integer, ForeignKey("process_result.id_process"), primary_key=True)

    model = relationship("Model", back_populates="model_data")
    process_result = relationship("ProcessResult", back_populates="model_data")

# Validation Result: Stores the evaluation results of the model during validation.
class ValidationResult(Base):
    __tablename__ = "validation_result"
    id_validation = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("model.id_model"))
    accuracy = Column(Float)
    matrix_id = Column(Integer)
    metrics_id = Column(Integer)

    model = relationship("Model", back_populates="validation_results")
    validation_data = relationship("ValidationData", back_populates="validation_result")

# Validation Data: Stores whether a piece of data was correctly classified during validation.
class ValidationData(Base):
    __tablename__ = "validation_data"
    id_validation = Column(Integer, ForeignKey("validation_result.id_validation"), primary_key=True)
    id_process = Column(Integer, ForeignKey("process_result.id_process"), primary_key=True)
    is_correct = Column(Boolean)

    validation_result = relationship("ValidationResult", back_populates="validation_data")
    process_result = relationship("ProcessResult", back_populates="validation_data")

# Confusion Matrix: Stores confusion matrix data for both processing (training) and validation.
class ConfusionMatrix(Base):
    __tablename__ = "confusion_matrix"
    matrix_id = Column(Integer, primary_key=True)
    label_id = Column(Integer, ForeignKey("label_emotion.id_label"), primary_key=True)
    predicted_label_id = Column(Integer, ForeignKey("label_emotion.id_label"), primary_key=True)
    total = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint('matrix_id', 'label_id', 'predicted_label_id', name='uix_confusion_matrix'),
    )

# Class Metrics: Stores the precision and recall for each label during both processing and validation.
class ClassMetrics(Base):
    __tablename__ = "class_metrics"
    metrics_id = Column(Integer, primary_key=True)
    label_id = Column(Integer, ForeignKey("label_emotion.id_label"), primary_key=True)
    precision = Column(Float)
    recall = Column(Float)

    __table_args__ = (
        UniqueConstraint('metrics_id', 'label_id', name='uix_class_metrics'),
    )
