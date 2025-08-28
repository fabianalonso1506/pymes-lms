from pydantic import BaseModel
from typing import Optional


class PositionBase(BaseModel):
    name: str
    description: Optional[str] = None


class PositionCreate(PositionBase):
    pass


class PositionRead(PositionBase):
    id: int

    class Config:
        orm_mode = True
