from sqlalchemy import Column, Integer, ForeignKey
from ..db.session import Base


class PositionCompetency(Base):
    __tablename__ = "position_competencies"
    position_id = Column(Integer, ForeignKey("positions.id", ondelete="CASCADE"), primary_key=True)
    competency_id = Column(Integer, ForeignKey("competencies.id", ondelete="CASCADE"), primary_key=True)
    required_level = Column(Integer)
