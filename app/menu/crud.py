from sqlalchemy.orm import Session
from app.menu import models as menu_models  # 部门模型
from app.menu import schemas
from typing import Optional
from sqlalchemy.exc import IntegrityError
from core.exceptions import BusinessException
from fastapi import status


def get_menu(db: Session, menu_id: int):
    return db.query(menu_models.Menu).filter(menu_models.Menu.id == menu_id).first()


def get_menus(db: Session, skip: int = 0, limit: int = 100):
    return db.query(menu_models.Menu).offset(skip).limit(limit).all()


def get_menus_by_parent(db: Session, parent_id: Optional[int] = None):
    query = db.query(menu_models.Menu)
    if parent_id is None:
        query = query.filter(menu_models.Menu.parent_id.is_(None))
    else:
        query = query.filter(menu_models.Menu.parent_id == parent_id)
    return query.order_by(menu_models.Menu.order).all()


def is_descendant(db: Session, parent_id: int, child_id: int) -> bool:
    """
    检查 child_id 是否是 parent_id 的子孙节点
    """
    current_id = parent_id
    while current_id:
        if current_id == child_id:
            return True
        menu = get_menu(db, current_id)
        if not menu or not menu.parent_id:
            break
        current_id = menu.parent_id
    return False


def create_menu(db: Session, menu: schemas.MenuCreate):
    try:
        db_menu = menu_models.Menu(**menu.model_dump())
        db.add(db_menu)
        db.commit()
        db.refresh(db_menu)
        return db_menu
    except IntegrityError as e:
        db.rollback()
        raise BusinessException(
            entity="user",
            error_type="database_error",
            details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def update_menu(db: Session, menu_id: int, menu: schemas.MenuUpdate):
    db_menu = get_menu(db, menu_id)
    if not db_menu:
        raise BusinessException(
            entity="菜单",
            error_type="不存在",
            status_code=status.HTTP_404_NOT_FOUND
        )
        # 检查循环依赖
    if menu.parent_id is not None:
        if menu.parent_id == menu_id:  # 直接循环
            raise BusinessException(
                entity="菜单",
                error_type="循环依赖",
                details="不能将菜单设置为其自身的父菜单",
                status_code=status.HTTP_400_BAD_REQUEST
            )

            # 检查多级循环
        current_parent = get_menu(db, menu.parent_id)
        if current_parent:
            # 检查是否尝试将父菜单设置为子菜单
            if is_descendant(db, menu.parent_id, menu_id):
                raise BusinessException(
                    entity="菜单",
                    error_type="循环依赖",
                    details="不能将父菜单设置为其子菜单的下级",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
        try:
            update_data = menu.model_dump(exclude_unset=True)
            for field in update_data:
                setattr(db_menu, field, update_data[field])

            db.commit()
            db.refresh(db_menu)
            return db_menu
        except IntegrityError as e:
            db.rollback()
            raise BusinessException(
                entity="user",
                error_type="database_error",
                details=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


def delete_menu(db: Session, menu_id: int):
    db_menu = get_menu(db, menu_id)
    if not db_menu:
        return False

    db.delete(db_menu)
    db.commit()
    return True
