from fastapi import APIRouter, HTTPException, Depends
from app.services.auth import create_access_token, authenticate_user
from app import database, schemas
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/login", response_model=schemas.Token)
def login(user_data: schemas.UserBase, db: Session = Depends(database.get_db)):
    user = authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect Username or Password")
    
    token = create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer"}
