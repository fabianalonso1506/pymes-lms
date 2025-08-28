import os
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from fastapi.testclient import TestClient
from ..main import app
from ..db.session import Base, engine, SessionLocal
from ..models import User
from ..core.security import get_password_hash

client = TestClient(app)


def setup_module():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    user = User(name="Tester", email="tester@example.com", role="empleado", hashed_password=get_password_hash("secret"))
    db.add(user)
    db.commit()
    db.close()


def teardown_module():
    Base.metadata.drop_all(bind=engine)


def test_login():
    response = client.post("/api/auth/login", data={"username": "tester@example.com", "password": "secret"})
    assert response.status_code == 200
    assert "access_token" in response.json()
