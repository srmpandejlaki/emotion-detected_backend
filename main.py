from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import engine
from app.models.models import Base
from app.routers import all_routers

# Buat database jika belum ada
Base.metadata.create_all(bind=engine)

# Inisialisasi FastAPI
app = FastAPI(
    title="Emotion Classification API",
    description="Backend API for Sentiment Analysis App for Police Performance in Indonesia",
    version="1.0.0"
)

# melakukan konfigurasi CORS agar frontend dapat berkomunikasi dengan backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ganti dengan domain frontend jika sudah deploy
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# menambahkan semua router yang ada di routers/__init__.py
for router in all_routers:
    app.include_router(router)

# Endpoint Root
@app.get("/")
def read_root():
    return {"message": "Welcome to Emotion Classification API"}

