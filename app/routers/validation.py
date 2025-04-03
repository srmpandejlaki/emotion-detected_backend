from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ValidationResult, Dataset
from app.schemas import ValidationInput, ValidationResponse
from app.utils import predict_emotion, get_latest_model
from app.auth import get_current_user

router = APIRouter()

@router.post("/validation/single", response_model=ValidationResponse)
def validate_text(input_data: ValidationInput, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """Melakukan validasi emosi pada teks yang diberikan oleh pengguna."""
    model = get_latest_model()
    if not model:
        raise HTTPException(status_code=400, detail="Model belum tersedia")
    
    emotion = predict_emotion(input_data.text, model)
    
    # Simpan hasil klasifikasi ke dalam dataset sebagai data latih
    new_data = Dataset(text=input_data.text, label=emotion)
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    
    return {"emotion": emotion, "message": "Klasifikasi berhasil"}

@router.get("/validation/login-admin")
def login_as_admin():
    """Redirect ke halaman login admin."""
    return {"message": "Redirecting to admin login"}

@router.post("/logout")
def logout():
    """Menghapus sesi login pengguna."""
    return {"message": "Logout berhasil"}
