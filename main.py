from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router

app = FastAPI()

# Tambahkan middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # asal frontend kamu
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routing API
app.include_router(api_router)

# perintah untuk jalankan server
# uvicorn main:app --reload
