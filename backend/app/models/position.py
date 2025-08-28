from sqlalchemy import Column, Integer, String, Text
from ..db.session import Base


class Position(Base):
    __tablename__ = "positions"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
