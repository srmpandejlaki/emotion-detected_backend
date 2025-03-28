from fastapi import APIRouter
from app.services.classification import classify_text

router = APIRouter(prefix="/classification", tags=["Classification"])

@router.post("/")
def classify_comment(text: str):
    result = classify_text(text)
    return {"original_text": text, "emotion": result}
