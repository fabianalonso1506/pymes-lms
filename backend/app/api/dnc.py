from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db.session import get_db
from ..models import PositionCompetency, Competency, Course, Position
from ..schemas.dnc import DNCRequest, DNCResponse
from ..core.security import get_current_user

router = APIRouter(prefix="/dnc", tags=["dnc"])


@router.post("", response_model=DNCResponse)
def process_dnc(data: DNCRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    pcs = db.query(PositionCompetency, Competency).join(Competency, PositionCompetency.competency_id == Competency.id).filter(PositionCompetency.position_id == data.position_id).all()
    gaps = {"cognitive": [], "psychomotor": [], "affective": []}
    for pc, comp in pcs:
        level = data.competency_levels.get(comp.id, 0)
        if level < (pc.required_level or 0):
            gaps[comp.domain.value].append(comp.name)
    courses = db.query(Course).filter(Course.target_position_id == data.position_id).all()
    mandatory = [c.id for c in courses if c.mandatory]
    optional = [c.id for c in courses if not c.mandatory]
    return DNCResponse(gaps=gaps, mandatory_courses=mandatory, optional_courses=optional)
