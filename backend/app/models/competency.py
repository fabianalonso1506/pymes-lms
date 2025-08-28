from sqlalchemy import Column, Integer, String, Enum
from ..db.session import Base
import enum


class Domain(str, enum.Enum):
    cognitive = "cognitive"
    psychomotor = "psychomotor"
    affective = "affective"


class Competency(Base):
    __tablename__ = "competencies"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    domain = Column(Enum(Domain), nullable=False)
    level_required = Column(Integer)
