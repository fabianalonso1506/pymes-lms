from pydantic import BaseModel
from typing import Optional, Any


class AssessmentItemBase(BaseModel):
    assessment_id: int
    stem: str
    type: str
    options_json: Any
    answer_key: Optional[str] = None


class AssessmentItemCreate(AssessmentItemBase):
    pass


class AssessmentItemRead(AssessmentItemBase):
    id: int

    class Config:
        orm_mode = True
