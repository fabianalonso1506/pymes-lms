from pydantic import BaseModel
from typing import Dict


class DNCRequest(BaseModel):
    position_id: int
    competency_levels: Dict[int, int]


class DNCResponse(BaseModel):
    gaps: Dict[str, list[str]]
    mandatory_courses: list[int]
    optional_courses: list[int]
