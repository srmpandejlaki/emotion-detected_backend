from sqlalchemy import Column, Integer, String, DateTime, func
from app.utils.database import Base

class DatasetKomentar(Base):
    __tablename__ = "dataset_komentar"

    id = Column(Integer, primary_key=True, index=True)
    komentar = Column(String, nullable=False)
    label = Column(String, nullable=True)  # Label emosi setelah klasifikasi
    created_at = Column(DateTime, default=func.now())
