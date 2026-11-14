
import logging
from typing import Any

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


class AIServiceError(Exception):
    """Raised when the independent COSMOCare AI service is unavailable."""


def generate_ai_response(
    message: str,
    context: dict[str, Any] | None = None,
    history: list[dict[str, str]] | None = None,
) -> dict[str, str]:

    if not settings.INTERNAL_API_TOKEN:
        raise AIServiceError("AI service authentication is not configured.")

    url = f"{settings.AI_SERVICE_URL}/internal/generate"

    headers = {
        "X-Internal-Token": settings.INTERNAL_API_TOKEN,
        "Content-Type": "application/json",
    }

    payload = {
        "message": message,
        "context": context,
        "history": history or [],
    }

    try:
        with httpx.Client(timeout=settings.AI_SERVICE_TIMEOUT) as client:
            response = client.post(
                url,
                headers=headers,
                json=payload,
            )

        response.raise_for_status()

        result = response.json()

        answer = result.get("answer")
        model = result.get("model")

        if not isinstance(answer, str) or not answer.strip():
            raise AIServiceError("AI service returned an invalid response.")

        return {
            "answer": answer.strip(),
            "model": str(model or "unknown"),
        }

    except httpx.TimeoutException as exc:
        logger.warning("COSMOCare AI service request timed out.")
        raise AIServiceError("AI service request timed out.") from exc

    except httpx.HTTPStatusError as exc:
        logger.error(
            "COSMOCare AI service returned HTTP %s.",
            exc.response.status_code,
        )
        raise AIServiceError("AI service returned an error.") from exc

    except httpx.RequestError as exc:
        logger.error(
            "Could not connect to COSMOCare AI service: %s",
            type(exc).__name__,
        )
        raise AIServiceError("AI service is unavailable.") from exc

    except ValueError as exc:
        logger.error("COSMOCare AI service returned invalid JSON.")
        raise AIServiceError("AI service returned invalid data.") from exc
