from pydantic import BaseModel
from typing import Optional, Any


class RubricBase(BaseModel):
    module_id: int
    criteria_json: Any
    weight_percent: Optional[int] = None


class RubricCreate(RubricBase):
    pass


class RubricRead(RubricBase):
    id: int

    class Config:
        orm_mode = True
