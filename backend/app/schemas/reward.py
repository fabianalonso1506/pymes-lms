from pydantic import BaseModel
from typing import Optional


class RewardBase(BaseModel):
    name: str
    cost_points: Optional[int] = None
    description: Optional[str] = None


class RewardCreate(RewardBase):
    pass


class RewardRead(RewardBase):
    id: int

    class Config:
        orm_mode = True
