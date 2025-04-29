from sqlalchemy import Column, Integer, String, Boolean, Text, Float, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship
from app.database.config import Base
from datetime import datetime

# Label Emotions: Labels for emotions used in the system.
class LabelEmotion(Base):
    __tablename__ = "label_emotion"
    id_label = Column(Integer, primary_key=True, index=True)
    nama_label = Column(String(50), nullable=False)

    # Relationship to DataCollection and ProcessResult
    data_collection = relationship("DataCollection", back_populates="label")
    process_results_auto = relationship("ProcessResult", back_populates="auto_label", foreign_keys="[ProcessResult.automatic_label]")

# Data Collection: Holds the text data and its emotion.
class DataCollection(Base):
    __tablename__ = "data_collection"
    id_data = Column(Integer, primary_key=True, index=True)
    text_data = Column(String, nullable=False)
    emotion = Column(String, nullable=True)

    # Relationships to LabelEmotion and ProcessResult
    label_emotion = relationship("LabelEmotion", back_populates="data", uselist=False)
    processing_result = relationship("ProcessResult", back_populates="data", uselist=False)

# Process Result: Stores the results of text preprocessing and automatic label assignment.
class ProcessResult(Base):
    __tablename__ = "process_result"
    id_process = Column(Integer, primary_key=True, index=True)
    id_data = Column(Integer, ForeignKey("data_collection.id_data"), nullable=False)
    text_preprocessing = Column(String, nullable=True)
    automatic_label = Column(Integer, ForeignKey("label_emotion.id_label"), nullable=True)

    # New columns for tracking processed data.
    is_processed = Column(Boolean, default=False)  # Marks whether this data has been used for training.
    processed_at = Column(DateTime, nullable=True)  # Stores the date when data was used for training.

    # Relationships to DataCollection
    data = relationship("DataCollection", back_populates="processing_result")

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
