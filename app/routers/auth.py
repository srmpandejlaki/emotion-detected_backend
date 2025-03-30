from fastapi import APIRouter, HTTPException, Depends
from app.utils.auth import create_token, verify_password
from app.schemas.user import UserLogin, UserResponse
from app.models.user import User
from app.utils.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=UserResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_data.username).first()
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_token(user.id)
    return {"username": user.username, "token": token}
