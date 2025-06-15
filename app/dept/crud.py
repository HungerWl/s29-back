from sqlalchemy.orm import Session
from app.dept import models, schemas
from uuid import UUID
from core.exceptions import BusinessException
from fastapi import status
from sqlalchemy.exc import IntegrityError


def get_dept_by_name(db: Session, name: str):
    return db.query(models.Dept).filter(models.Dept.name == name).first()


def get_dept_by_code(db: Session, code: str):
    return db.query(models.Dept).filter(models.Dept.code == code).first()


# 部门创建
def create_dept(db: Session, dept_in: schemas.DeptCreate):
    # 检查名称冲突
    if get_dept_by_name(db, dept_in.name):
        raise BusinessException(
            entity="部门名称",
            error_type="已存在",
        )
    if get_dept_by_code(db, dept_in.code):
        raise BusinessException(
            entity="部门编码",
            error_type="已存在",
        )

    try:
        dept = models.Dept(**dept_in.model_dump())
        db.add(dept)
        db.commit()
        db.refresh(dept)
        return dept
    except IntegrityError as e:
        db.rollback()
        raise BusinessException(
            entity="department",
            error_type="database_error",
            details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def get_dept(db: Session, dept_id: UUID):
    return db.query(models.Dept).filter(models.Dept.id == dept_id).first()


def get_all_dept(db: Session):
    return db.query(models.Dept).order_by(models.Dept.code.asc()).all()


# 部门更新
def update_dept(db: Session, dept_id: UUID, dept_in: schemas.DeptUpdate):
    # 先获取要更新的部门（使用str转换）
    db_dept = db.query(models.Dept).filter(models.Dept.id == str(dept_id)).first()
    if not db_dept:
        raise BusinessException(
            entity="部门",
            error_type="不存在",
            status_code=status.HTTP_404_NOT_FOUND
        )

    # 检查名称冲突（排除自己）
    existing_name_dept = get_dept_by_name(db, dept_in.name)
    if existing_name_dept and str(existing_name_dept.id) != str(dept_id):
        raise BusinessException(
            entity="部门名称",
            error_type="已存在",
            status_code=status.HTTP_400_BAD_REQUEST
        )

    # 检查编码冲突（排除自己）
    existing_code_dept = get_dept_by_code(db, dept_in.code)
    if existing_code_dept and str(existing_code_dept.id) != str(dept_id):
        raise BusinessException(
            entity="部门编码",
            error_type="已存在",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    try:
        # 更新字段
        update_data = dept_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_dept, key, value)

        db.commit()
        db.refresh(db_dept)
        return db_dept
    except IntegrityError as e:
        db.rollback()
        raise BusinessException(
            entity="department",
            error_type="database_error",
            details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# 部门删除
def delete_dept(db: Session, dept_id: UUID):
    # 获取要删除的部门
    dept = db.query(models.Dept).filter(models.Dept.id == str(dept_id)).first()
    if not dept:
        return None

    try:
        # 递归删除所有子部门
        def delete_children(parent_id):
            children = db.query(models.Dept).filter(models.Dept.parent_id == parent_id).all()
            for child in children:
                delete_children(str(child.id))  # 递归删除子部门
                db.delete(child)  # 删除当前子部门

        # 先删除所有子部门
        delete_children(str(dept_id))

        # 最后删除当前部门
        db.delete(dept)
        db.commit()
        return dept
    except Exception as e:
        db.rollback()
        raise BusinessException(
            entity="department",
            error_type="delete_error",
            details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
