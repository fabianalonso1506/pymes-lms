from sqlalchemy import Column, Integer, String, ForeignKey
from ..db.session import Base


class Module(Base):
    __tablename__ = "modules"
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"))
    title = Column(String, nullable=False)
    order = Column(Integer, nullable=False)
    weight_percent = Column(Integer)
