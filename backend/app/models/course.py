from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from ..db.session import Base


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    mandatory = Column(Boolean, default=False)
    target_position_id = Column(Integer, ForeignKey("positions.id", ondelete="SET NULL"))
