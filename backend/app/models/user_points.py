from sqlalchemy import Column, Integer, ForeignKey
from ..db.session import Base


class UserPoints(Base):
    __tablename__ = "user_points"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    points = Column(Integer, default=0)
