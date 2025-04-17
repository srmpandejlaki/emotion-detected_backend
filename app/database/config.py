from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DB_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

    # Path model Naive Bayes dan data evaluasi
    MODEL_DIR: str = "app/models"
    MODEL_FILE: str = "naive_bayes_model.pkl"
    METRICS_FILE: str = "metrics.json"
    TEST_DATA_FILE: str = "data_uji.csv"

    # Path untuk model BERT dan lexicon (untuk langkah lanjutan)
    BERT_MODEL_PATH: str = "app/models/bert_model"
    LEXICON_FILE: str = "app/lexicons/lexicon.json"

    @property
    def model_path(self):
        return os.path.join(self.MODEL_DIR, self.MODEL_FILE)

    @property
    def metrics_path(self):
        return os.path.join(self.MODEL_DIR, self.METRICS_FILE)

    @property
    def test_data_path(self):
        return os.path.join(self.MODEL_DIR, self.TEST_DATA_FILE)

    @property
    def bert_model_path(self):
        return self.BERT_MODEL_PATH

    @property
    def lexicon_path(self):
        return self.LEXICON_FILE

settings = Settings()
