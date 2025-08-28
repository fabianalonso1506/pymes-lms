from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from ..db.session import Base


class AssessmentItem(Base):
    __tablename__ = "assessment_items"
    id = Column(Integer, primary_key=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id", ondelete="CASCADE"))
    stem = Column(String, nullable=False)
    type = Column(String, nullable=False)
    options_json = Column(JSON)
    answer_key = Column(String)
