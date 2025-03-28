from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.utils.database import Base

class HasilKlasifikasi(Base):
    __tablename__ = "hasil_klasifikasi"

    id = Column(Integer, primary_key=True, index=True)
    komentar_id = Column(Integer, ForeignKey("dataset_komentar.id"), nullable=False)
    hasil_klasifikasi = Column(String, nullable=False)  # Positif, Negatif, Netral
    confidence_score = Column(String, nullable=True)  # Skor keyakinan model
    classified_at = Column(DateTime, default=func.now())

    komentar = relationship("DatasetKomentar", backref="hasil_klasifikasi")
