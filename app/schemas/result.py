from pydantic import BaseModel

class ClassificationResult(BaseModel):
    text: str  # Komentar yang diklasifikasikan
    predicted_emotion: str  # Hasil prediksi emosi (positif/negatif/netral)
    confidence: float  # Probabilitas hasil klasifikasi

class ClassificationResponse(ClassificationResult):
    id: int  # ID database untuk menyimpan hasil klasifikasi
    class Config:
        from_attributes = True
