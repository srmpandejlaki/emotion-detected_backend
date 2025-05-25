# src/models.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from src.database.config import Base


class Dataset(Base):
    __tablename__ = 'datasets'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    emotion = Column(String, nullable=False)
    inserted_at = Column(DateTime, default=datetime.utcnow)

    preprocessed_data = relationship(
        "PreprocessedDataset", back_populates="dataset")


class PreprocessedDataset(Base):
    __tablename__ = 'preprocessed_datasets'

    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, ForeignKey('datasets.id'))
    text = Column(String, nullable=False)
    preprocessed_text = Column(String)
    emotion = Column(String, nullable=False)
    is_preprocessed = Column(Boolean, default=False)
    is_trained = Column(Boolean, default=False)
    inserted_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    dataset = relationship("Dataset", back_populates="preprocessed_data")


class Model(Base):
    __tablename__ = 'models'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    model_path = Column(String)
    total_data = Column(Integer)
    test_size = Column(Float)
    accuracy = Column(Float)
    train_time = Column(Float)

    # Paths to training results (stored as files)
    prior_probabilities_path = Column(String)
    word_probabilities_path = Column(String)
    tfidf_details_path = Column(String)
    bert_lexicon_details_path = Column(String)
    evaluation_metrics_path = Column(String)
    predict_results_path = Column(String)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
