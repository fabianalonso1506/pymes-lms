from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from ..db.session import Base
import enum


class UserRole(str, enum.Enum):
    empleado = "empleado"
    lider = "lider"
    rrhh = "rrhh"
    capacitador = "capacitador"
    admin = "admin"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    role = Column(Enum(UserRole), default=UserRole.empleado, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
