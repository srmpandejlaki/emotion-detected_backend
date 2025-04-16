from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DB_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

    # Tambahan untuk path model dan data
    MODEL_DIR: str = "app/models"
    MODEL_FILE: str = "naive_bayes_model.pkl"
    METRICS_FILE: str = "metrics.json"
    TEST_DATA_FILE: str = "data_uji.csv"

    @property
    def model_path(self):
        return os.path.join(self.MODEL_DIR, self.MODEL_FILE)

    @property
    def metrics_path(self):
        return os.path.join(self.MODEL_DIR, self.METRICS_FILE)

    @property
    def test_data_path(self):
        return os.path.join(self.MODEL_DIR, self.TEST_DATA_FILE)

settings = Settings()
