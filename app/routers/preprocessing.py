from fastapi import APIRouter
from app.services.preprocess import preprocess_text

router = APIRouter(prefix="/preprocess", tags=["Preprocessing"])

@router.post("/")
def preprocess_comment(text: str):
    cleaned_text = preprocess_text(text)
    return {"original_text": text, "cleaned_text": cleaned_text}
