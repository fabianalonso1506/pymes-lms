from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from ..models.certificate import CertificateType


class CertificateBase(BaseModel):
    user_id: int
    course_id: int
    type: CertificateType
    issued_at: Optional[datetime] = None
    folio: Optional[str] = None


class CertificateCreate(CertificateBase):
    pass


class CertificateRead(CertificateBase):
    id: int

    class Config:
        orm_mode = True
