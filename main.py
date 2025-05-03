from fastapi import FastAPI
from app.database.config import engine, Base
from app.api.routes import (
    data_collection_router,
    preprocessing_router, 
    processing_router
)

# Inisialisasi aplikasi FastAPI
app = FastAPI()

# Create the database tables if they do not exist
Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(data_collection_router, prefix="/data-collection", tags=["DataCollection"])
app.include_router(preprocessing_router, prefix="/preprocessing", tags=["Preprocessing"])
app.include_router(processing_router, prefix="/processing", tags=["Processing"])
