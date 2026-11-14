
from typing import Any, Literal

from pydantic import BaseModel, Field


class ConversationMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=10000)


class GenerateRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10000)
    context: dict[str, Any] | None = None
    history: list[ConversationMessage] = Field(
        default_factory=list,
        max_length=12,
    )


class GenerateResponse(BaseModel):
    answer: str
    model: str
