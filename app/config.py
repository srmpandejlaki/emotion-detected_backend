import os
from dotenv import load_dotenv

# Load variabel lingkungan dari .env
load_dotenv()

class Config:
    # Konfigurasi Database
    DATABASE_URL = os.getenv("DB_URL", "postgresql://user:password@localhost/emotiondb")

    # Konfigurasi Aplikasi
    APP_NAME = "Emotion Classification API"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # Secret Key (untuk autentikasi jika diperlukan)
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")

config = Config()
