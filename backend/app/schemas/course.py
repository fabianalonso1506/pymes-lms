from pydantic import BaseModel
from typing import Optional


class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    mandatory: bool = False
    target_position_id: Optional[int] = None


class CourseCreate(CourseBase):
    pass


class CourseRead(CourseBase):
    id: int

    class Config:
        orm_mode = True
