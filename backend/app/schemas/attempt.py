from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AttemptBase(BaseModel):
    assessment_id: int
    user_id: int
    score: Optional[int] = None
    passed: Optional[bool] = None


class AttemptCreate(BaseModel):
    answers: dict[int, str]


class AttemptRead(AttemptBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class AttemptResult(AttemptRead):
    allow_retake: bool
