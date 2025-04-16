from sqlalchemy import Column, Integer, String, Boolean, Text, Float, ForeignKey, UniqueConstraint, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from app.database.base import Base


class LabelEmotion(Base):
    __tablename__ = "label_emotion"
    id_label = Column(Integer, primary_key=True, index=True)
    nama_label = Column(String(50), nullable=False)


class DataCollection(Base):
    __tablename__ = "data_collection"
    id_data = Column(Integer, primary_key=True, index=True)
    text_data = Column(Text, nullable=False)
    label_id = Column(Integer, ForeignKey("label_emotion.id_label"))


class ProcessResult(Base):
    __tablename__ = "process_result"
    id_process = Column(Integer, primary_key=True, index=True)
    id_data = Column(Integer, ForeignKey("data_collection.id_data"))
    text_preprocessing = Column(Text, nullable=False)
    is_training_data = Column(Boolean, nullable=False)
    automatic_label = Column(Integer, ForeignKey("label_emotion.id_label"))


class Model(Base):
    __tablename__ = "model"
    id_model = Column(Integer, primary_key=True, index=True)
    ratio_data = Column(String(10), nullable=False)
    accuracy = Column(Float)
    matrix_id = Column(Integer)
    metrics_id = Column(Integer)


class ModelData(Base):
    __tablename__ = "model_data"
    id_model = Column(Integer, ForeignKey("model.id_model"), primary_key=True)
    id_process = Column(Integer, ForeignKey("process_result.id_process"), primary_key=True)


class ValidationResult(Base):
    __tablename__ = "validation_result"
    id_validation = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("model.id_model"))
    accuracy = Column(Float)
    matrix_id = Column(Integer)
    metrics_id = Column(Integer)


class ValidationData(Base):
    __tablename__ = "validation_data"
    id_validation = Column(Integer, ForeignKey("validation_result.id_validation"), primary_key=True)
    id_process = Column(Integer, ForeignKey("process_result.id_process"), primary_key=True)
    is_correct = Column(Boolean)


class ConfusionMatrix(Base):
    __tablename__ = "confusion_matrix"
    matrix_id = Column(Integer, primary_key=True)
    label_id = Column(Integer, ForeignKey("label_emotion.id_label"), primary_key=True)
    predicted_label_id = Column(Integer, ForeignKey("label_emotion.id_label"), primary_key=True)
    total = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint('matrix_id', 'label_id', 'predicted_label_id', name='uix_confusion_matrix'),
    )


class ClassMetrics(Base):
    __tablename__ = "class_metrics"
    metrics_id = Column(Integer, primary_key=True)
    label_id = Column(Integer, ForeignKey("label_emotion.id_label"), primary_key=True)
    precision = Column(Float)
    recall = Column(Float)

    __table_args__ = (
        UniqueConstraint('metrics_id', 'label_id', name='uix_class_metrics'),
    )
