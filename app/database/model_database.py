from sqlalchemy import Column, Integer, String, Boolean, Text, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database.config import Base


class LabelEmotion(Base):
    __tablename__ = "label_emotion"
    id_label = Column(Integer, primary_key=True, index=True)
    nama_label = Column(String(50), nullable=False)

    # Relasi ke DataCollection dan ProcessResult
    data_collection = relationship("DataCollection", back_populates="label")
    process_results_auto = relationship("ProcessResult", back_populates="auto_label", foreign_keys="[ProcessResult.automatic_label]")


class DataCollection(Base):
    __tablename__ = "data_collection"
    id_data = Column(Integer, primary_key=True, index=True)
    text_data = Column(Text, nullable=False)
    label_id = Column(Integer, ForeignKey("label_emotion.id_label"))

    # Relasi ke label_emotion
    label = relationship("LabelEmotion", back_populates="data_collection")

    # Relasi ke ProcessResult
    process_results = relationship("ProcessResult", back_populates="data")


class ProcessResult(Base):
    __tablename__ = "process_result"
    id_process = Column(Integer, primary_key=True, index=True)
    id_data = Column(Integer, ForeignKey("data_collection.id_data"))
    text_preprocessing = Column(Text, nullable=False)
    is_training_data = Column(Boolean, nullable=False)
    automatic_label = Column(Integer, ForeignKey("label_emotion.id_label"))

    # Relasi ke data_collection
    data = relationship("DataCollection", back_populates="process_results")

    # Relasi ke label_emotion
    auto_label = relationship("LabelEmotion", back_populates="process_results_auto", foreign_keys=[automatic_label])

    # Relasi ke model_data dan validation_data
    model_data = relationship("ModelData", back_populates="process_result")
    validation_data = relationship("ValidationData", back_populates="process_result")


class Model(Base):
    __tablename__ = "model"
    id_model = Column(Integer, primary_key=True, index=True)
    ratio_data = Column(String(10), nullable=False)
    accuracy = Column(Float)
    matrix_id = Column(Integer)
    metrics_id = Column(Integer)

    model_data = relationship("ModelData", back_populates="model")
    validation_results = relationship("ValidationResult", back_populates="model")


class ModelData(Base):
    __tablename__ = "model_data"
    id_model = Column(Integer, ForeignKey("model.id_model"), primary_key=True)
    id_process = Column(Integer, ForeignKey("process_result.id_process"), primary_key=True)

    model = relationship("Model", back_populates="model_data")
    process_result = relationship("ProcessResult", back_populates="model_data")


class ValidationResult(Base):
    __tablename__ = "validation_result"
    id_validation = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("model.id_model"))
    accuracy = Column(Float)
    matrix_id = Column(Integer)
    metrics_id = Column(Integer)

    model = relationship("Model", back_populates="validation_results")
    validation_data = relationship("ValidationData", back_populates="validation_result")


class ValidationData(Base):
    __tablename__ = "validation_data"
    id_validation = Column(Integer, ForeignKey("validation_result.id_validation"), primary_key=True)
    id_process = Column(Integer, ForeignKey("process_result.id_process"), primary_key=True)
    is_correct = Column(Boolean)

    validation_result = relationship("ValidationResult", back_populates="validation_data")
    process_result = relationship("ProcessResult", back_populates="validation_data")


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
