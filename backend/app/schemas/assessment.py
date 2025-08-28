from pydantic import BaseModel
from typing import Optional
from ..models.assessment import AssessmentType


class AssessmentBase(BaseModel):
    module_id: int
    type: AssessmentType
    pass_score: Optional[int] = None


class AssessmentCreate(AssessmentBase):
    pass


class AssessmentRead(AssessmentBase):
    id: int

    class Config:
        orm_mode = True
