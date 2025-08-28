import os
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from fastapi.testclient import TestClient
from ..main import app
from ..db.session import Base, engine, SessionLocal
from ..models import User, Course, Module, Assessment, AssessmentItem
from ..core.security import get_password_hash

client = TestClient(app)


def setup_module():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    user = User(name="Eval", email="eval@example.com", role="empleado", hashed_password=get_password_hash("secret"))
    db.add(user)
    course = Course(title="Test Course", mandatory=True)
    db.add(course)
    db.flush()
    module = Module(course_id=course.id, title="M1", order=1)
    db.add(module)
    db.flush()
    assessment = Assessment(module_id=module.id, type="summative", pass_score=80)
    db.add(assessment)
    db.flush()
    item1 = AssessmentItem(assessment_id=assessment.id, stem="Q1", type="multiple_choice", options_json=["A","B"], answer_key="A")
    item2 = AssessmentItem(assessment_id=assessment.id, stem="Q2", type="multiple_choice", options_json=["A","B"], answer_key="B")
    db.add_all([item1, item2])
    db.commit()
    db.close()


def teardown_module():
    Base.metadata.drop_all(bind=engine)


def test_attempt_scoring_and_retake():
    res = client.post("/api/auth/login", data={"username": "eval@example.com", "password": "secret"})
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    attempt_res = client.post(
        "/api/assessments/1/attempts",
        json={"answers": {1: "A", 2: "A"}},
        headers=headers,
    )
    body = attempt_res.json()
    assert body["score"] == 50
    assert body["allow_retake"] is True
    attempt_res2 = client.post(
        "/api/assessments/1/attempts",
        json={"answers": {1: "A", 2: "B"}},
        headers=headers,
    )
    assert attempt_res2.json()["score"] == 100
