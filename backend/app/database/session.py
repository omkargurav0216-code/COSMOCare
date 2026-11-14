
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from app.core.config import settings


# --------------------------------------------------
# DATABASE ENGINE
# --------------------------------------------------

# SQLite requires check_same_thread=False when
# database connections are used across FastAPI threads.
connect_args = (
    {"check_same_thread": False}
    if settings.DATABASE_URL.startswith("sqlite")
    else {}
)

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
    future=True,
)


# --------------------------------------------------
# DATABASE SESSION
# --------------------------------------------------

# Each request receives its own database session.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


# --------------------------------------------------
# SQLALCHEMY BASE MODEL
# --------------------------------------------------

# All database entities inherit from this Base.
Base = declarative_base()


# --------------------------------------------------
# DATABASE DEPENDENCY
# --------------------------------------------------

def get_db() -> Generator[Session, None, None]:
    """
    Provide a database session to FastAPI endpoints.

    The session is automatically closed after
    the request has been processed.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
