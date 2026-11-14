
from sqlalchemy.orm import Session

from app.models.entities import Message


def get_recent_conversation_history(
    db: Session,
    conversation_id: str,
    limit: int = 12,
) -> list[dict[str, str]]:
    """
    Retrieve recent conversation messages in chronological order.
    """

    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.desc(), Message.id.desc())
        .limit(limit)
        .all()
    )

    messages.reverse()

    return [
        {
            "role": message.role,
            "content": message.content,
        }
        for message in messages
        if message.role in ("user", "assistant")
    ]


def save_message(
    db: Session,
    conversation_id: str,
    role: str,
    content: str,
) -> Message:
    """
    Save a user or assistant message to the existing messages table.
    """

    if role not in ("user", "assistant"):
        raise ValueError("Invalid conversation message role.")

    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
    )

    db.add(message)
    db.flush()

    return message
