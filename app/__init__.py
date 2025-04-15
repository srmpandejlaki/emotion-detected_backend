from fastapi import FastAPI
from app.routers import auth, dataset, preprocessing, training, validation
from app.database.database import engine, Base

# Inisialisasi database
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Emotion Classification API")

# Register routers
app.include_router(auth.router)
app.include_router(dataset.router)
app.include_router(preprocessing.router)
app.include_router(training.router)
app.include_router(validation.router)