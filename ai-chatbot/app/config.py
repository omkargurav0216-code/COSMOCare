import os
from pathlib import Path

from dotenv import load_dotenv

# Load the .env file from the ai-chatbot directory,
# regardless of the terminal's current working directory.
AI_SERVICE_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(AI_SERVICE_ROOT / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip()
INTERNAL_API_TOKEN = os.getenv("INTERNAL_API_TOKEN", "").strip()

# Groq fallback provider
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-20b",
).strip()
GROQ_TIMEOUT = int(os.getenv("GROQ_TIMEOUT", "45"))