from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from ..db.session import Base
import enum


class CertificateType(str, enum.Enum):
    internal = "internal"
    DC3_stub = "DC3_stub"


class Certificate(Base):
    __tablename__ = "certificates"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"))
    type = Column(Enum(CertificateType), nullable=False)
    issued_at = Column(DateTime)
    folio = Column(String)
