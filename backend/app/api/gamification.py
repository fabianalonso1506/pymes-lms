from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.session import get_db
from ..models import UserPoints, Reward, Redemption, RedemptionStatus, User
from ..schemas import Points, RankingEntry, RedemptionCreate, RedemptionRead, RedemptionUpdate, RewardRead
from ..core.security import get_current_user, RoleChecker

router = APIRouter(prefix="/gamification", tags=["gamification"])

points_map = {"micro": 5, "activity": 10, "assessment": 20}

def _change_points(db: Session, user_id: int, delta: int):
    record = db.query(UserPoints).get(user_id)
    if record:
        record.points += delta
    else:
        record = UserPoints(user_id=user_id, points=delta)
        db.add(record)
    db.commit()


def _get_medal(points: int) -> str:
    if points >= 200:
        return "oro"
    if points >= 100:
        return "plata"
    return "bronce"


@router.post("/award", response_model=Points)
def award(data: dict, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    action = data.get("action")
    pts = points_map.get(action)
    if not pts:
        raise HTTPException(status_code=400, detail="Invalid action")
    _change_points(db, current_user.id, pts)
    total = db.query(UserPoints).get(current_user.id).points
    return Points(points=total, medal=_get_medal(total))


@router.get("/points", response_model=Points)
def get_points(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    record = db.query(UserPoints).get(current_user.id)
    total = record.points if record else 0
    return Points(points=total, medal=_get_medal(total))


@router.get("/ranking", response_model=list[RankingEntry])
def ranking(role: str | None = None, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    q = db.query(UserPoints, User).join(User, UserPoints.user_id == User.id).order_by(UserPoints.points.desc())
    if role:
        q = q.filter(User.role == role)
    rows = q.all()
    return [RankingEntry(user_id=u.id, name=u.name, role=u.role.value if hasattr(u.role, 'value') else u.role, points=p.points) for p, u in rows]


@router.get("/rewards", response_model=list[RewardRead])
def list_rewards(db: Session = Depends(get_db)):
    return db.query(Reward).all()


@router.post("/redeem/{reward_id}", response_model=RedemptionRead)
def redeem(reward_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    reward = db.query(Reward).get(reward_id)
    if not reward:
        raise HTTPException(status_code=404, detail="Reward not found")
    record = db.query(UserPoints).get(current_user.id)
    points = record.points if record else 0
    if reward.cost_points and points < reward.cost_points:
        raise HTTPException(status_code=400, detail="Not enough points")
    _change_points(db, current_user.id, -reward.cost_points)
    redemption = Redemption(user_id=current_user.id, reward_id=reward_id)
    db.add(redemption)
    db.commit()
    db.refresh(redemption)
    return redemption


@router.get("/redemptions", response_model=list[RedemptionRead])
def my_redemptions(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(Redemption).filter(Redemption.user_id == current_user.id).all()


admin_required = RoleChecker(["rrhh", "lider", "admin"])

@router.get("/redemptions/pending", response_model=list[RedemptionRead], dependencies=[Depends(admin_required)])
def pending_redemptions(db: Session = Depends(get_db)):
    return db.query(Redemption).filter(Redemption.status == RedemptionStatus.pending).all()


@router.put("/redemptions/{redemption_id}", response_model=RedemptionRead, dependencies=[Depends(admin_required)])
def update_redemption(redemption_id: int, data: RedemptionUpdate, db: Session = Depends(get_db)):
    red = db.query(Redemption).get(redemption_id)
    if not red:
        raise HTTPException(status_code=404, detail="Redemption not found")
    red.status = data.status
    db.commit()
    db.refresh(red)
    return red
