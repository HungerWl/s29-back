from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.menu import schemas, crud
from core.database import get_db
from core.schemas.base import BaseResponse
from typing import List, Optional

menu_router = APIRouter(prefix="/menu", tags=["菜单管理"])


@menu_router.post(
    "/create",
    response_model=BaseResponse[schemas.MenuOut],
    summary="创建菜单",
    description="创建新菜单"
)
def create(menu_in: schemas.MenuCreate, db: Session = Depends(get_db)):
    menu = crud.create_menu(db, menu_in)
    return {"data": menu, "message": "菜单创建成功"}


@menu_router.get(
    "/list",
    response_model=BaseResponse[List[schemas.MenuOut]],
    summary="获取菜单树",
    description="获取所有菜单并以树形结构返回"
)
def get_menu_tree(menu_id: Optional[int] = None, db: Session = Depends(get_db)):
    menus = crud.get_menus_tree(db, menu_id)
    return {"data": menus, "message": "菜单获取成功"}


@menu_router.get(
    "/getRouter",
    response_model=BaseResponse[List[schemas.MenuOut]],
    summary="获取菜单树",
    description="获取所有菜单并以树形结构返回"
)
def get_menu_tree(menu_id: Optional[int] = None, db: Session = Depends(get_db)):
    menus = crud.get_menus_tree(db, menu_id)
    return {"data": menus, "message": "菜单获取成功"}


@menu_router.put(
    "/update/{menu_id}",
    response_model=BaseResponse[schemas.MenuOut],
    summary="更新菜单",
    description="更新指定菜单的信息"
)
def update_menu(
        menu_id: int,
        menu_in: schemas.MenuUpdate,
        db: Session = Depends(get_db)
):
    menu = crud.update_menu(db, menu_id, menu_in)
    return {"data": menu, "message": "菜单更新成功"}


@menu_router.delete(
    "/delete/{menu_id}",
    response_model=BaseResponse[None],
    summary="删除菜单",
    description="删除指定菜单"
)
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    crud.delete_menu(db, menu_id)
    return {"data": None, "message": "菜单删除成功"}
