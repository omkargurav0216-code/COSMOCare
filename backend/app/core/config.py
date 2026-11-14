
import os
from pathlib import Path

from dotenv import load_dotenv


# Resolve the backend directory independently of the terminal's
# current working directory.
BACKEND_ROOT = Path(__file__).resolve().parents[2]

# Load backend/.env. Existing system environment variables
# take precedence over values in the .env file.
load_dotenv(BACKEND_ROOT / ".env")


def parse_bool(value: str, default: bool = False) -> bool:
    """Convert environment variable strings into Boolean values."""

    normalized = value.strip().lower()

    if normalized in {"true", "1", "yes", "on"}:
        return True

    if normalized in {"false", "0", "no", "off"}:
        return False

    raise ValueError(
        f"Invalid Boolean environment variable: {value}"
    )


class Settings:
    """Central application configuration."""

    APP_NAME: str = os.getenv(
        "APP_NAME",
        "COSMOCare API"
    )

    API_VERSION: str = os.getenv(
        "API_VERSION",
        "v1"
    )

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./cosmocare.db"
    )

    CORS_ORIGINS: str = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173"
    )

    ML_SRC_PATH: str = os.getenv(
        "ML_SRC_PATH",
        "../ml/src"
    )

    SEED_DATABASE: bool = parse_bool(
        os.getenv("SEED_DATABASE", "true"),
        default=True
    )

    @property
    def cors_origins(self) -> list[str]:
        """Return configured frontend origins as a list."""

        return [
            origin.strip()
            for origin in self.CORS_ORIGINS.split(",")
            if origin.strip()
        ]


# Shared configuration instance used throughout the application.
settings = Settings()
