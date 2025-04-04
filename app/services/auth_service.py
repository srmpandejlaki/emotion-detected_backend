from datetime import timedelta
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
from app import models, database
from app.utils.token_utils import create_access_token, decode_token
from app.utils.security_utils import hash_password, verify_password
from app.utils.token_blacklist import is_token_blacklisted, add_to_blacklist
import os

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not verify_password(password, user.password):
        return None
    return user

def generate_access_token(user_id: int):
    return create_access_token(user_id=user_id, expire_minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        if is_token_blacklisted(token):
            raise credentials_exception
        payload = decode_token(token)
        user_id = int(payload.get("sub"))
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception

def logout_user(token: str):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=400, detail="Token already invalidated")
    add_to_blacklist(token)
