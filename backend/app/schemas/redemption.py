from pydantic import BaseModel
from datetime import datetime
from ..models.redemption import RedemptionStatus


class RedemptionCreate(BaseModel):
    reward_id: int


class RedemptionUpdate(BaseModel):
    status: RedemptionStatus


class RedemptionRead(BaseModel):
    id: int
    user_id: int
    reward_id: int
    status: RedemptionStatus
    created_at: datetime

    class Config:
        orm_mode = True
