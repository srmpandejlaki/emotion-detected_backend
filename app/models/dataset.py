from sqlalchemy import Column, Integer, String, ForeignKey
from app.utils.database import Base

class DatasetKomentar(Base):
    __tablename__ = "dataset_komentar"

    id = Column(Integer, primary_key=True, index=True)
    komentar = Column(String, nullable=False)
    label = Column(Integer, ForeignKey("label_emosi.id"), nullable=True) 
