from fastapi import FastAPI
from app.database.database import engine, Base
from app.api.routers import classification_router, validation_router, dataset_router
from app.services.model_service import check_model_availability

# Inisialisasi aplikasi FastAPI
app = FastAPI()

# Create the database tables if they do not exist
Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(classification_router.router)
app.include_router(validation_router.router)
app.include_router(dataset_router.router)

# Endpoint untuk mengecek status model
@app.get("/model/status")
def model_status():
    model_available, message = check_model_availability()
    return {"model_available": model_available, "message": message}

