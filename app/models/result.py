from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.utils.database import Base

class HasilKlasifikasi(Base):
    __tablename__ = "hasil_klasifikasi"

    id = Column(Integer, primary_key=True, index=True)
    komentar_id = Column(Integer, ForeignKey("dataset_komentar.id"), nullable=False)
    # hasil_klasifikasi berisi nomor 1-7
    hasil_klasifikasi = Column(Integer, ForeignKey("label_emosi.id"), nullable=False)  
    # Skor keyakinan model
    confidence_score = Column(String, nullable=True)  
    # Waktu klasifikasi
    classified_at = Column(DateTime, default=func.now())

    komentar = relationship("DatasetKomentar", backref="hasil_klasifikasi")
    label_emosi = relationship("LabelEmosi", backref="hasil_klasifikasi")
