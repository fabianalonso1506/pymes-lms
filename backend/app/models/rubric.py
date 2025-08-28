from sqlalchemy import Column, Integer, ForeignKey, JSON
from ..db.session import Base


class Rubric(Base):
    __tablename__ = "rubrics"
    id = Column(Integer, primary_key=True)
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"))
    criteria_json = Column(JSON)
    weight_percent = Column(Integer)
