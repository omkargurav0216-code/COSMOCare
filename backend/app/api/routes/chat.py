
from uuid import uuid4
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.entities import Astronaut, Conversation
from app.schemas.api import ChatIn, ChatOut
from app.core.config import settings

from app.services.ai_client import (
    generate_ai_response,
    AIServiceError,
)
from app.services.chat_context_service import build_astronaut_context
from app.services.conversation_service import (
    get_recent_conversation_history,
    save_message,
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/chat", response_model=ChatOut)
def chat(
    payload: ChatIn,
    db: Session = Depends(get_db),
):
    try:
        # 1. Find or create the conversation.
        conversation = (
            db.get(Conversation, payload.conversation_id)
            if payload.conversation_id
            else None
        )

        if payload.conversation_id and conversation is None:
            raise HTTPException(404, "Conversation not found.")

        if (
            conversation is not None
            and payload.astronaut_id
            and conversation.astronaut_id != payload.astronaut_id
        ):
            raise HTTPException(
                409,
                "Conversation astronaut does not match.",
            )

        if conversation is None:
            conversation = Conversation(
                id=str(uuid4()),
                astronaut_id=payload.astronaut_id,
            )
            db.add(conversation)
            db.flush()

        # Retain the astronaut associated with an existing conversation.
        astronaut_id = (
            payload.astronaut_id or conversation.astronaut_id
        )

        # 2. Validate the astronaut, if one is associated.
        if astronaut_id and not db.get(Astronaut, astronaut_id):
            raise HTTPException(404, "Astronaut not found.")

        # 3. Retrieve previous conversation history BEFORE saving
        #    the current user message.
        history = get_recent_conversation_history(
            db,
            conversation.id,
            limit=12,
        )

        # 4. Retrieve astronaut context when available.
        context = None

        if astronaut_id:
            context = build_astronaut_context(
                db,
                astronaut_id,
            )

        # 5. Save the current user message.
        save_message(
            db,
            conversation.id,
            "user",
            payload.message,
        )

        # 6. Generate the AI response.
        if settings.CHAT_MOCK_MODE:
            astronaut_name = (
                context.get("astronaut", {}).get("name", "the mission crew")
                if context
                else "the mission crew"
            )

            ai_result = {
                "answer": (
                    f"[MOCK RESPONSE]\n\n"
                    f"Hello! I'm COSMOCare Assistant. "
                    f"I received your question: '{payload.message}'.\n\n"
                    f"Current context: {astronaut_name}.\n\n"
                    "This is a simulated response used to verify the "
                    "COSMOCare chat integration. No live Gemini request "
                    "was made."
                ),
                "model": "mock-model",
            }
        else:
            ai_result = generate_ai_response(
                message=payload.message,
                context=context,
                history=history,
            )

        # 7. Save the assistant response.
        save_message(
            db,
            conversation.id,
            "assistant",
            ai_result["answer"],
        )

        # 8. Commit both messages together.
        db.commit()

        return ChatOut(
            conversation_id=conversation.id,
            status="completed",
            message=ai_result["answer"],
        )

    except HTTPException:
        db.rollback()
        raise

    except AIServiceError as exc:
        db.rollback()

        logger.warning(
            "Chat request could not be completed: %s",
            str(exc),
        )

        raise HTTPException(
            status_code=503,
            detail=(
                "COSMOCare AI is temporarily unavailable. "
                "Your message was not saved. Please try again later."
            ),
        ) from exc

    except Exception:
        db.rollback()

        logger.exception("Unexpected error while processing chat.")

        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while processing your message.",
        )

# from uuid import uuid4
# from fastapi import APIRouter,Depends,HTTPException
# from sqlalchemy.orm import Session
# from app.database.session import get_db
# from app.models.entities import Astronaut,Conversation,Message
# from app.schemas.api import ChatIn,ChatOut
# router=APIRouter()
# @router.post("/chat",response_model=ChatOut)
# def chat(payload:ChatIn,db:Session=Depends(get_db)):
#     if payload.astronaut_id and not db.get(Astronaut,payload.astronaut_id): raise HTTPException(404,"Astronaut not found")
#     conversation=db.get(Conversation,payload.conversation_id) if payload.conversation_id else None
#     if payload.conversation_id and conversation is None:
#         raise HTTPException(404,"Conversation not found")
#     if conversation is not None and payload.astronaut_id and conversation.astronaut_id != payload.astronaut_id:
#         raise HTTPException(409,"Conversation astronaut does not match")
#     if conversation is None:
#         conversation=Conversation(id=str(uuid4()),astronaut_id=payload.astronaut_id); db.add(conversation); db.flush()
#     db.add(Message(conversation_id=conversation.id,role="user",content=payload.message))
#     db.commit()
#     # AI developer owns the provider/model adapter. This endpoint is a stable handoff contract.
#     return ChatOut(conversation_id=conversation.id,status="integration_pending",
#       message="Your message was saved. AI assistant provider is not connected yet.")
