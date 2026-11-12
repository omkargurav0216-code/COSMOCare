import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    APP_NAME = os.getenv("APP_NAME", "COSMOCare API")
    API_VERSION = os.getenv("API_VERSION", "v1")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cosmocare.db")
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173")
    ML_SRC_PATH = os.getenv("ML_SRC_PATH", "../ml/src")
    SEED_DATABASE = os.getenv("SEED_DATABASE", "true").lower() == "true"

    @property
    def cors_origins(self):
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

settings = Settings()
