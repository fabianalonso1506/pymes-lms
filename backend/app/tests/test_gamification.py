import os
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from fastapi.testclient import TestClient
from ..main import app
from ..db.session import Base, engine, SessionLocal
from ..models import User, Reward
from ..core.security import get_password_hash

client = TestClient(app)


def setup_module():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    user = User(name="Gamer", email="gamer@example.com", role="empleado", hashed_password=get_password_hash("secret"))
    hr = User(name="HR", email="hr@example.com", role="rrhh", hashed_password=get_password_hash("secret"))
    reward = Reward(name="Vale", cost_points=10)
    db.add_all([user, hr, reward])
    db.commit()
    db.close()


def teardown_module():
    Base.metadata.drop_all(bind=engine)


def _login(email):
    res = client.post("/api/auth/login", data={"username": email, "password": "secret"})
    return res.json()["access_token"]


def test_award_and_redeem_flow():
    token = _login("gamer@example.com")
    headers = {"Authorization": f"Bearer {token}"}
    client.post("/api/gamification/award", json={"action": "micro"}, headers=headers)
    client.post("/api/gamification/award", json={"action": "activity"}, headers=headers)
    client.post("/api/gamification/award", json={"action": "assessment"}, headers=headers)
    pts = client.get("/api/gamification/points", headers=headers).json()
    assert pts["points"] >= 35
    redeem = client.post("/api/gamification/redeem/1", headers=headers)
    assert redeem.status_code == 200
    red_id = redeem.json()["id"]
    hr_token = _login("hr@example.com")
    hr_headers = {"Authorization": f"Bearer {hr_token}"}
    client.put(f"/api/gamification/redemptions/{red_id}", json={"status": "approved"}, headers=hr_headers)
    redemptions = client.get("/api/gamification/redemptions", headers=headers).json()
    assert redemptions[0]["status"] == "approved"
