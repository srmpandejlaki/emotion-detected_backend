from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app import models
from passlib.context import CryptContext

# konfigurasi JWT
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# hashing password & token authentication
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# hashing password function
def has_password(password: str):
    return pwd_context.hash(password)

# verifying password function
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# authentication function 
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not verify_password(password, user.password):
        return None
    return user

# token generation function
def create_access_token(user_id: int):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# token verification function
def get_current_user(token: str, db: Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            return None
        return db.query(models.User).filter(models.User.id == user_id).first()
    except JWTError:
        return None
