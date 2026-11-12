import os
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
os.environ["DATABASE_URL"]="sqlite:///./test_cosmocare.db"
os.environ["SEED_DATABASE"]="true"
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.session import Base,engine
@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=engine); Base.metadata.create_all(bind=engine)
    with TestClient(app) as c: yield c
    Base.metadata.drop_all(bind=engine)
