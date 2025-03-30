from fastapi import FastAPI
from app.database import engine, Base
from app.routers import user, dataset, validation

# Inisialisasi database
Base.metadata.create_all(bind=engine)

# Inisialisasi aplikasi FastAPI
app = FastAPI()

# Include Routers
app.include_router(user.router)
app.include_router(dataset.router)
app.include_router(validation.router)
