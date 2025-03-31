from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

class EmotionLabel(Base):
    __tablename__ = "emotion_labels"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

class Dataset(Base):
    __tablename__ = "dataset"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    label_id = Column(Integer, ForeignKey("emotion_labels.id"), nullable=True)
    
    label = relationship("EmotionLabel")

class ValidationResult(Base):
    __tablename__ = "validation_results"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    label_id = Column(Integer, ForeignKey("emotion_labels.id"), nullable=False)
    accuracy = Column(Integer, nullable=False)
    precision = Column(Integer, nullable=False)
    recall = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    label = relationship("EmotionLabel")
