from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..db.session import Base


class Attempt(Base):
    __tablename__ = "attempts"
    id = Column(Integer, primary_key=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    score = Column(Integer)
    passed = Column(Boolean)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
