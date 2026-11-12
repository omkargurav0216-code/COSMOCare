from app.database.session import Base,engine,SessionLocal
from app.models import entities
def init_db():
    Base.metadata.create_all(bind=engine)
    from app.core.config import settings
    if settings.SEED_DATABASE:
        from app.database.seed import seed_database
        with SessionLocal() as db: seed_database(db)
