from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from core.schemas.base import BaseResponse
from core.exceptions import BusinessException
from app.menu import schemas, crud
from core.database import get_db

menu_router = APIRouter(
    prefix="/menu",
    tags=["菜单管理"]
)


@menu_router.post(
    "/create",
    response_model=BaseResponse[schemas.MenuInDB],
    summary="创建菜单",
    description="创建新的菜单项，需提供菜单名称、路由路径等必填字段。"
)
def create_menu(menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    """
    创建菜单

    - **menu_type**: 菜单类型（如 'menu' 或 'button'）
    - **menu_name**: 菜单名称（必填）
    - **route_path**: 路由地址（必填）
    - 其他字段为可选参数
    """
    try:
        menu = crud.create_menu(db=db, menu=menu)
        return {"data": menu, "message": "菜单创建成功"}
    except BusinessException as e:
        raise e


@menu_router.get(
    "/list",
    response_model=BaseResponse[List[schemas.MenuInDB]],
    summary="获取菜单列表",
    description="分页查询菜单列表，支持 skip 和 limit 参数。"
)
def read_menus(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    获取菜单列表

    - **skip**: 跳过的记录数（默认 0）
    - **limit**: 每页返回的记录数（默认 100）
    """
    try:
        menus = crud.get_menus(db, skip=skip, limit=limit)
        return {"data": menus}
    except BusinessException as e:
        raise e


@menu_router.get(
    "/tree",
    response_model=BaseResponse[List[schemas.MenuInDB]],
    summary="获取菜单树",
    description="根据 parent_id 获取菜单树结构，不传 parent_id 则返回顶级菜单。"
)
def read_menu_tree(parent_id: int = None, db: Session = Depends(get_db)):
    """
    获取菜单树

    - **parent_id**: 父级菜单ID（可选，不传则返回顶级菜单）
    """
    try:
        menus = crud.get_menus_by_parent(db, parent_id=parent_id)
        return {"data": menus}
    except BusinessException as e:
        raise e


@menu_router.get(
    "/{menu_id}",
    response_model=BaseResponse[schemas.MenuInDB],
    summary="获取菜单详情",
    description="根据菜单ID获取菜单详细信息。"
)
def read_menu(menu_id: int, db: Session = Depends(get_db)):
    """
    获取菜单详情

    - **menu_id**: 菜单ID（路径参数）
    """
    db_menu = crud.get_menu(db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="菜单不存在")
    return {"data": db_menu}


@menu_router.put(
    "/update/{menu_id}",
    response_model=BaseResponse[schemas.MenuInDB],
    summary="更新菜单",
    description="根据菜单ID更新菜单信息。"
)
def update_menu(menu_id: int, menu: schemas.MenuUpdate, db: Session = Depends(get_db)):
    """
    更新菜单

    - **menu_id**: 菜单ID（路径参数）
    - **请求体**: 可更新的菜单字段（部分更新支持）
    """
    try:
        db_menu = crud.update_menu(db, menu_id=menu_id, menu=menu)
        return {"data": db_menu, "message": "菜单更新成功"}
    except BusinessException as e:
        raise e


@menu_router.delete(
    "/delete/{menu_id}",
    response_model=BaseResponse,
    summary="删除菜单",
    description="根据菜单ID删除菜单。"
)
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    """
    删除菜单

    - **menu_id**: 菜单ID（路径参数）
    """
    try:
        deleted_menu = crud.delete_menu(db, menu_id)
        return {"data": deleted_menu, "message": "菜单删除成功"}
    except BusinessException as e:
        raise e
