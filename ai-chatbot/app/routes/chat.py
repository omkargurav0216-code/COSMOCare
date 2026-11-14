
import secrets

from fastapi import APIRouter, Header, HTTPException, status

from app.config import INTERNAL_API_TOKEN
from app.schemas.chat import GenerateRequest, GenerateResponse
from app.services.llm_client import (
    generate_response,
    ProviderConfigurationError,
    ProviderUnavailableError,
)

router = APIRouter(prefix="/internal", tags=["internal-ai"])


@router.post(
    "/generate",
    response_model=GenerateResponse,
)
async def generate(
    payload: GenerateRequest,
    internal_token: str | None = Header(
        default=None,
        alias="X-Internal-Token",
    ),
):
    # Verify internal service authentication.
    if not INTERNAL_API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Internal API authentication is not configured.",
        )

    if not internal_token or not secrets.compare_digest(
        internal_token,
        INTERNAL_API_TOKEN,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid internal service token.",
        )

    try:
        answer, model = await generate_response(
            message=payload.message,
            context=payload.context,
            history=payload.history,
        )

        return GenerateResponse(
            answer=answer,
            model=model,
        )

    except ProviderConfigurationError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc

    except ProviderUnavailableError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="All configured AI providers failed to generate a response.",
        ) from exc
