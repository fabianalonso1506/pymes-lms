import os
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from fastapi.testclient import TestClient
from ..main import app
from ..db.session import Base, engine, SessionLocal
from ..models import User, Course
from ..core.security import get_password_hash

client = TestClient(app)


def setup_module():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    user = User(name="Emp", email="emp@example.com", role="empleado", hashed_password=get_password_hash("secret"))
    hr = User(name="HR", email="hr@example.com", role="rrhh", hashed_password=get_password_hash("secret"))
    course = Course(title="Curso", mandatory=True)
    db.add_all([user, hr, course])
    db.commit()
    db.close()


def teardown_module():
    Base.metadata.drop_all(bind=engine)


def _login(email):
    res = client.post("/api/auth/login", data={"username": email, "password": "secret"})
    return res.json()["access_token"]


def test_issue_and_download():
    hr_token = _login("hr@example.com")
    hr_headers = {"Authorization": f"Bearer {hr_token}"}
    res = client.post("/api/certificates/issue", json={"user_id": 1, "course_id": 1, "type": "internal"}, headers=hr_headers)
    cert_id = res.json()["id"]
    user_token = _login("emp@example.com")
    user_headers = {"Authorization": f"Bearer {user_token}"}
    certs = client.get("/api/certificates/my", headers=user_headers).json()
    assert len(certs) == 1
    html = client.get(f"/api/certificates/{cert_id}/download", headers=user_headers)
    assert html.status_code == 200
    assert "Constancia" in html.text
