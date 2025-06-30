from sqlalchemy.orm import Session, joinedload
from app.menu import schemas
from app.menu import models as menu_models
from core.exceptions import BusinessException
from fastapi import status
from sqlalchemy.exc import IntegrityError
from typing import List, Optional


def create_menu(db: Session, menu_in: schemas.MenuCreate) -> menu_models.Menu:
    """
    创建菜单
    :param db: 数据库会话
    :param menu_in: 菜单创建数据
    :return: 创建后的菜单对象
    """
    try:
        db_menu = menu_models.Menu(**menu_in.model_dump())
        db.add(db_menu)
        db.commit()
        db.refresh(db_menu)
        return db_menu
    except IntegrityError as e:
        db.rollback()
        raise BusinessException(
            entity="menu",
            error_type="database_error",
            details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def get_menus_tree(db: Session, menu_id: Optional[int] = None) -> List[menu_models.Menu]:
    """
    获取菜单树形结构
    :param db: 数据库会话
    :param menu_id: 指定获取某一个菜单（含子菜单），为空时获取所有菜单树
    :return: 树形结构菜单列表
    """
    if menu_id:
        # 查询指定菜单及其子菜单
        menus = db.query(menu_models.Menu).options(
            joinedload(menu_models.Menu.children).joinedload(menu_models.Menu.children)
        ).filter(menu_models.Menu.id == menu_id).all()
    else:
        # 查询所有顶级菜单及其子菜单
        menus = db.query(menu_models.Menu).options(
            joinedload(menu_models.Menu.children).joinedload(menu_models.Menu.children)
        ).filter(menu_models.Menu.parent_id == None).all()

    return menus


# Add these functions to crud.py

def update_menu(db: Session, menu_id: int, menu_in: schemas.MenuUpdate) -> menu_models.Menu:
    """
    更新菜单
    :param db: 数据库会话
    :param menu_id: 要更新的菜单ID
    :param menu_in: 菜单更新数据
    :return: 更新后的菜单对象
    """
    db_menu = db.query(menu_models.Menu).filter(menu_models.Menu.id == menu_id).first()
    if not db_menu:
        raise BusinessException(
            entity="menu",
            error_type="not_found",
            details="Menu not found",
            status_code=status.HTTP_404_NOT_FOUND
        )

    try:
        update_data = menu_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_menu, key, value)

        db.commit()
        db.refresh(db_menu)
        return db_menu
    except IntegrityError as e:
        db.rollback()
        raise BusinessException(
            entity="menu",
            error_type="database_error",
            details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def delete_menu(db: Session, menu_id: int) -> None:
    """
    删除菜单
    :param db: 数据库会话
    :param menu_id: 要删除的菜单ID
    """
    db_menu = db.query(menu_models.Menu).filter(menu_models.Menu.id == menu_id).first()
    if not db_menu:
        raise BusinessException(
            entity="menu",
            error_type="not_found",
            details="Menu not found",
            status_code=status.HTTP_404_NOT_FOUND
        )

    try:
        db.delete(db_menu)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise BusinessException(
            entity="menu",
            error_type="database_error",
            details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
