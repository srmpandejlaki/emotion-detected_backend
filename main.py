from fastapi import FastAPI
from app.database.session import engine, Base
from app.api.routes.preprocessing_router import preprocessing_router
from app.api.routes.processing_router import processing_router

# Inisialisasi aplikasi FastAPI
app = FastAPI()

# Create the database tables if they do not exist
Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(preprocessing_router, prefix="/preprocessing", tags=["Preprocessing"])
app.include_router(processing_router, prefix="/processing", tags=["Processing"])
