from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from ..db.session import get_db
from ..models import Certificate, CertificateType, User, Course
from ..schemas import CertificateCreate, CertificateRead
from ..core.security import get_current_user, RoleChecker

router = APIRouter(prefix="/certificates", tags=["certificates"])

admin_required = RoleChecker(["rrhh", "lider", "admin"])

@router.post("/issue", response_model=CertificateRead, dependencies=[Depends(admin_required)])
def issue_certificate(data: CertificateCreate, db: Session = Depends(get_db)):
    cert = Certificate(
        user_id=data.user_id,
        course_id=data.course_id,
        type=data.type,
        issued_at=data.issued_at or datetime.utcnow(),
        folio=data.folio or f"FOL-{int(datetime.utcnow().timestamp())}",
    )
    db.add(cert)
    db.commit()
    db.refresh(cert)
    return cert


@router.get("/my", response_model=list[CertificateRead])
def my_certificates(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(Certificate).filter(Certificate.user_id == current_user.id).all()


@router.get("/{cert_id}/download")
def download_certificate(cert_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    cert = db.query(Certificate).get(cert_id)
    if not cert or cert.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Certificate not found")
    user = db.query(User).get(cert.user_id)
    course = db.query(Course).get(cert.course_id)
    html = f"""
    <html><body>
    <h1>Constancia {cert.type}</h1>
    <p>{user.name} completó {course.title} el {cert.issued_at.strftime('%Y-%m-%d')}</p>
    <p>Folio: {cert.folio}</p>
    </body></html>
    """
    return HTMLResponse(content=html)
