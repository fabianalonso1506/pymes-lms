from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.session import get_db
from ..models import Assessment, AssessmentItem, Attempt, UserPoints
from ..schemas.attempt import AttemptCreate, AttemptResult
from ..core.security import get_current_user

router = APIRouter(prefix="/assessments", tags=["evaluation"])


@router.post("/{assessment_id}/attempts", response_model=AttemptResult)
def submit_attempt(assessment_id: int, data: AttemptCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    assessment = db.query(Assessment).get(assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    items = db.query(AssessmentItem).filter(AssessmentItem.assessment_id == assessment_id).all()
    correct = 0
    for item in items:
        answer = data.answers.get(item.id)
        if answer is not None and answer == item.answer_key:
            correct += 1
    score = int((correct / len(items)) * 100) if items else 0
    passed = score >= (assessment.pass_score or 0)
    attempt = Attempt(assessment_id=assessment_id, user_id=current_user.id, score=score, passed=passed)
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    if passed:
        record = db.query(UserPoints).get(current_user.id)
        if record:
            record.points += 20
        else:
            db.add(UserPoints(user_id=current_user.id, points=20))
        db.commit()
    allow_retake = score < 80
    return AttemptResult(
        id=attempt.id,
        assessment_id=attempt.assessment_id,
        user_id=attempt.user_id,
        score=attempt.score,
        passed=attempt.passed,
        created_at=attempt.created_at,
        allow_retake=allow_retake,
    )


@router.get("/{assessment_id}/attempts", response_model=list[AttemptResult])
def list_attempts(assessment_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    attempts = db.query(Attempt).filter(Attempt.assessment_id == assessment_id, Attempt.user_id == current_user.id).all()
    return [AttemptResult(**a.__dict__, allow_retake=a.score < 80) for a in attempts]
