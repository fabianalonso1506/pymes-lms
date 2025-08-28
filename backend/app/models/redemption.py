from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.sql import func
from ..db.session import Base
import enum


class RedemptionStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class Redemption(Base):
    __tablename__ = "redemptions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    reward_id = Column(Integer, ForeignKey("rewards.id", ondelete="CASCADE"))
    status = Column(Enum(RedemptionStatus), default=RedemptionStatus.pending, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
