from sqlalchemy import Column, Integer, String
from app.utils.database import Base

class LabelEmosi(Base):
    __tablename__ = "label_emosi"

    id = Column(Integer, primary_key=True, index=True)
    nama_emosi = Column(String, unique=True, nullable=False)
