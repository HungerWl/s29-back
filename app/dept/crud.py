# apps/dept/crud.py

from sqlalchemy.orm import Session
from app.dept import models, schemas
from uuid import UUID
from fastapi import HTTPException


def create_dept(db: Session, dept_in: schemas.DeptCreate):
    # 验证父部门是否存在
    if dept_in.parent_id:
        parent = db.query(models.Dept).filter(models.Dept.id == str(dept_in.parent_id)).first()
        if not parent:
            raise HTTPException(status_code=400, detail="Parent department not found")

    dept = models.Dept(**dept_in.model_dump())
    db.add(dept)
    db.commit()
    db.refresh(dept)
    return dept


def get_dept(db: Session, dept_id: UUID):
    return db.query(models.Dept).filter(models.Dept.id == dept_id).first()


def get_all_dept(db: Session):
    return db.query(models.Dept).order_by(models.Dept.code.asc()).all()


def update_dept(db: Session, dept_id: UUID, dept_in: schemas.DeptUpdate):
    db_dept = db.query(models.Dept).filter(models.Dept.id == str(dept_id)).first()
    if not db_dept:
        return None
    for key, value in dept_in.model_dump(exclude_unset=True).items():
        setattr(db_dept, key, value)
    db.commit()
    db.refresh(db_dept)
    return db_dept


def delete_dept(db: Session, dept_id: UUID):
    dept = db.query(models.Dept).filter(models.Dept.id == str(dept_id)).first()
    if dept:
        db.delete(dept)
        db.commit()
    return dept


def delete_dept(db: Session, dept_id: UUID):
    dept = db.query(models.Dept).filter(models.Dept.id == str(dept_id)).first()
    if dept:
        db.delete(dept)
        db.commit()
    return dept
