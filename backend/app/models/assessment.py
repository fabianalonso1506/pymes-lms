from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from ..db.session import Base
import enum


class AssessmentType(str, enum.Enum):
    diagnostic = "diagnostic"
    formative = "formative"
    summative = "summative"


class Assessment(Base):
    __tablename__ = "assessments"
    id = Column(Integer, primary_key=True)
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"))
    type = Column(Enum(AssessmentType), nullable=False)
    pass_score = Column(Integer)
