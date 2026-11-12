from uuid import uuid4
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.entities import Astronaut,Conversation,Message
from app.schemas.api import ChatIn,ChatOut
router=APIRouter()
@router.post("/chat",response_model=ChatOut)
def chat(payload:ChatIn,db:Session=Depends(get_db)):
    if payload.astronaut_id and not db.get(Astronaut,payload.astronaut_id): raise HTTPException(404,"Astronaut not found")
    conversation=db.get(Conversation,payload.conversation_id) if payload.conversation_id else None
    if payload.conversation_id and conversation is None:
        raise HTTPException(404,"Conversation not found")
    if conversation is not None and payload.astronaut_id and conversation.astronaut_id != payload.astronaut_id:
        raise HTTPException(409,"Conversation astronaut does not match")
    if conversation is None:
        conversation=Conversation(id=str(uuid4()),astronaut_id=payload.astronaut_id); db.add(conversation); db.flush()
    db.add(Message(conversation_id=conversation.id,role="user",content=payload.message))
    db.commit()
    # AI developer owns the provider/model adapter. This endpoint is a stable handoff contract.
    return ChatOut(conversation_id=conversation.id,status="integration_pending",
      message="Your message was saved. AI assistant provider is not connected yet.")
