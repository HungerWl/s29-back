from sqlalchemy.orm import Session
from starlette import status
from app.role import models, schemas
from uuid import UUID
from sqlalchemy.exc import IntegrityError
from core.exceptions import BusinessException


def get_role_by_name(db: Session, name: str):
    return db.query(models.Role).filter(models.Role.name == name).first()


def get_role(db: Session, role_id: UUID):
    return db.query(models.Role).filter(models.Role.id == str(role_id)).first()


def create_role(db: Session, role_in: schemas.RoleCreate):
    if get_role_by_name(db, role_in.name):
        raise BusinessException(
            entity="角色名称",
            error_type="已存在",
        )
    # 检查权限字符是否已存在
    existing_role = db.query(models.Role).filter(
        models.Role.permission_key == role_in.permission_key
    ).first()
    if existing_role:
        raise BusinessException(
            entity="权限字符",
            error_type="已存在",
        )
    try:
        role = models.Role(**role_in.model_dump())
        db.add(role)
        db.commit()
        db.refresh(role)
        return role
    except IntegrityError as e:
        db.rollback()
        raise BusinessException(
            entity="department",
            error_type="database_error",
            details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def get_all_role(db: Session):
    return db.query(models.Role).order_by(models.Role.name.asc()).all()


def update_role(db: Session, role_id: UUID, role_in: schemas.RoleUpdate):
    role = get_role(db, role_id)
    if not role:
        raise BusinessException(
            entity="角色",
            error_type="不存在",
            status_code=status.HTTP_404_NOT_FOUND
        )

    # 检查角色名称是否已存在（排除当前角色）
    if role_in.name and role_in.name != role.name:
        if get_role_by_name(db, role_in.name):
            raise BusinessException(
                entity="角色名称",
                error_type="已存在",
            )

    # 检查权限字符是否已存在（排除当前角色）
    if role_in.permission_key and role_in.permission_key != role.permission_key:
        existing_role = db.query(models.Role).filter(
            models.Role.permission_key == role_in.permission_key,
            models.Role.id != str(role_id)  # 排除当前角色
        ).first()
        print(existing_role, "existing_role")
        if existing_role:
            raise BusinessException(
                entity="权限字符",
                error_type="已存在",
            )

    try:
        update_data = role_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(role, key, value)
        db.commit()
        db.refresh(role)
        return role
    except IntegrityError as e:
        db.rollback()
        raise BusinessException(
            entity="role",
            error_type="database_error",
            details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def delete_role(db: Session, role_id: UUID):
    role = get_role(db, role_id)
    if not role:
        raise BusinessException(
            entity="角色",
            error_type="不存在",
            status_code=status.HTTP_404_NOT_FOUND
        )

    try:
        db.delete(role)
        db.commit()
        return role
    except IntegrityError as e:
        db.rollback()
        raise BusinessException(
            entity="role",
            error_type="database_error",
            details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
