from fastapi import FastAPI
from app.config import config
from app.routes import dataset, classification, preprocessing

# Inisialisasi FastAPI
app = FastAPI(title=config.APP_NAME, debug=config.DEBUG)

# Registrasi router API
app.include_router(dataset.router, prefix="/dataset", tags=["Dataset"])
app.include_router(classification.router, prefix="/classify", tags=["Classification"])
app.include_router(preprocessing.router, prefix="/preprocess", tags=["Preprocessing"])

# Endpoint utama
@app.get("/")
def home():
    return {"message": f"{config.APP_NAME} is running!", "debug_mode": config.DEBUG}

# Menjalankan aplikasi jika dijalankan secara langsung
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
