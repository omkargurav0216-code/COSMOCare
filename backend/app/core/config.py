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

    # Independent COSMOCare AI service
    AI_SERVICE_URL = os.getenv("AI_SERVICE_URL", "http://127.0.0.1:9000").rstrip("/")

    INTERNAL_API_TOKEN = os.getenv("INTERNAL_API_TOKEN", "").strip()

    AI_SERVICE_TIMEOUT = float(os.getenv("AI_SERVICE_TIMEOUT", "45"))

    CHAT_MOCK_MODE = os.getenv("CHAT_MOCK_MODE", "false").lower() == "true"

    HF_TOKEN = os.getenv("HF_TOKEN", "").strip()

    HF_MODEL = os.getenv(
        "HF_MODEL",
        "meta-llama/Llama-3.1-8B-Instruct",
    ).strip()

    HF_TIMEOUT = int(os.getenv("HF_TIMEOUT", "45"))

    @property
    def cors_origins(self):
        return [
            origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()
        ]


settings = Settings()

# import os
# from pathlib import Path

# from dotenv import load_dotenv


# # Resolve the backend directory independently of the terminal's
# # current working directory.
# BACKEND_ROOT = Path(__file__).resolve().parents[2]

# # Load backend/.env. Existing system environment variables
# # take precedence over values in the .env file.
# load_dotenv(BACKEND_ROOT / ".env")


# def parse_bool(value: str, default: bool = False) -> bool:
#     """Convert environment variable strings into Boolean values."""

#     normalized = value.strip().lower()

#     if normalized in {"true", "1", "yes", "on"}:
#         return True

#     if normalized in {"false", "0", "no", "off"}:
#         return False

#     raise ValueError(
#         f"Invalid Boolean environment variable: {value}"
#     )


# class Settings:
#     """Central application configuration."""

#     APP_NAME: str = os.getenv(
#         "APP_NAME",
#         "COSMOCare API"
#     )

#     API_VERSION: str = os.getenv(
#         "API_VERSION",
#         "v1"
#     )

#     DATABASE_URL: str = os.getenv(
#         "DATABASE_URL",
#         "sqlite:///./cosmocare.db"
#     )

#     CORS_ORIGINS: str = os.getenv(
#         "CORS_ORIGINS",
#         "http://localhost:5173"
#     )

#     ML_SRC_PATH: str = os.getenv(
#         "ML_SRC_PATH",
#         "../ml/src"
#     )

#     SEED_DATABASE: bool = parse_bool(
#         os.getenv("SEED_DATABASE", "true"),
#         default=True
#     )

#     @property
#     def cors_origins(self) -> list[str]:
#         """Return configured frontend origins as a list."""

#         return [
#             origin.strip()
#             for origin in self.CORS_ORIGINS.split(",")
#             if origin.strip()
#         ]


# # Shared configuration instance used throughout the application.
# settings = Settings()
