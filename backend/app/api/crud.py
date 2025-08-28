from typing import Type, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.session import get_db
from ..core.security import RoleChecker
from .. import models, schemas

admin_required = RoleChecker(["admin", "rrhh", "capacitador"])
router = APIRouter(prefix="/crud", tags=["crud"])


# Generic helper

def get_object(db: Session, model: Type, obj_id: int):
    obj = db.query(model).get(obj_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Item not found")
    return obj


# Users CRUD
@router.get("/users", response_model=List[schemas.UserRead], dependencies=[Depends(admin_required)])
def list_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@router.get("/users/{user_id}", response_model=schemas.UserRead, dependencies=[Depends(admin_required)])
def get_user(user_id: int, db: Session = Depends(get_db)):
    return get_object(db, models.User, user_id)


@router.put("/users/{user_id}", response_model=schemas.UserRead, dependencies=[Depends(admin_required)])
def update_user(user_id: int, user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    user = get_object(db, models.User, user_id)
    user.name = user_in.name
    user.email = user_in.email
    user.role = user_in.role
    if user_in.password:
        from ..core.security import get_password_hash
        user.hashed_password = get_password_hash(user_in.password)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/users/{user_id}", dependencies=[Depends(admin_required)])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = get_object(db, models.User, user_id)
    db.delete(user)
    db.commit()
    return {"ok": True}


# Helper to build CRUD for simple models

def simple_crud(model, create_schema, read_schema, prefix: str):
    @router.post(f"/{prefix}", response_model=read_schema, dependencies=[Depends(admin_required)])
    def create(item: create_schema, db: Session = Depends(get_db)):
        obj = model(**item.dict())
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @router.get(f"/{prefix}", response_model=List[read_schema], dependencies=[Depends(admin_required)])
    def list_items(db: Session = Depends(get_db)):
        return db.query(model).all()

    @router.get(f"/{prefix}/{{item_id}}", response_model=read_schema, dependencies=[Depends(admin_required)])
    def get_item(item_id: int, db: Session = Depends(get_db)):
        return get_object(db, model, item_id)

    @router.put(f"/{prefix}/{{item_id}}", response_model=read_schema, dependencies=[Depends(admin_required)])
    def update_item(item_id: int, item: create_schema, db: Session = Depends(get_db)):
        obj = get_object(db, model, item_id)
        for field, value in item.dict().items():
            setattr(obj, field, value)
        db.commit()
        db.refresh(obj)
        return obj

    @router.delete(f"/{prefix}/{{item_id}}", dependencies=[Depends(admin_required)])
    def delete_item(item_id: int, db: Session = Depends(get_db)):
        obj = get_object(db, model, item_id)
        db.delete(obj)
        db.commit()
        return {"ok": True}


# Register CRUD for entities
simple_crud(models.Position, schemas.PositionCreate, schemas.PositionRead, "positions")
simple_crud(models.Course, schemas.CourseCreate, schemas.CourseRead, "courses")
simple_crud(models.Module, schemas.ModuleCreate, schemas.ModuleRead, "modules")
simple_crud(models.Asset, schemas.AssetCreate, schemas.AssetRead, "assets")
simple_crud(models.Rubric, schemas.RubricCreate, schemas.RubricRead, "rubrics")
simple_crud(models.Assessment, schemas.AssessmentCreate, schemas.AssessmentRead, "assessments")
simple_crud(models.AssessmentItem, schemas.AssessmentItemCreate, schemas.AssessmentItemRead, "assessment_items")
simple_crud(models.Reward, schemas.RewardCreate, schemas.RewardRead, "rewards")
simple_crud(models.Certificate, schemas.CertificateCreate, schemas.CertificateRead, "certificates")
