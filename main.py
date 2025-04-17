from fastapi import FastAPI
from app.database.session import engine, Base
from app.api.routers.preprocessing_router import router as preprocessing_router

# Inisialisasi aplikasi FastAPI
app = FastAPI()

# Create the database tables if they do not exist
Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(preprocessing_router, prefix="/preprocessing", tags=["Preprocessing"])
