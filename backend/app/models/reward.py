from sqlalchemy import Column, Integer, String, Text
from ..db.session import Base


class Reward(Base):
    __tablename__ = "rewards"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cost_points = Column(Integer)
    description = Column(Text)
