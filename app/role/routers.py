from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict
from app.role import schemas, crud
from core.database import get_db
from uuid import UUID

role_router = APIRouter(prefix="/role", tags=["角色管理"])


@role_router.post(
    "/create",
    response_model=schemas.BaseResponse[schemas.RoleInDB],
    summary="创建角色",
    description="创建新角色"
)
def create(role_in: schemas.RoleCreate, db: Session = Depends(get_db)):
    post = crud.create_role(db, role_in)
    return {"data": post, "message": "角色创建成功"}


@role_router.get(
    "/list",
    response_model=schemas.BaseResponse[List[schemas.RoleInDB]],
    summary="获取角色列表",
)
def list_all(db: Session = Depends(get_db)):
    role = crud.get_all_role(db)
    return {"data": role}


@role_router.put(
    "/update/{role_id}",
    response_model=schemas.BaseResponse[schemas.RoleInDB],
    summary="更新角色",
    description="更新角色信息"
)
def update(role_id: UUID, role_in: schemas.RoleUpdate, db: Session = Depends(get_db)):
    role = crud.update_role(db, role_id, role_in)
    return {"data": role, "message": "角色更新成功"}


@role_router.delete(
    "/delete/{role_id}",
    response_model=schemas.BaseResponse[schemas.RoleInDB],
    summary="删除角色",
    description="删除指定角色"
)
def delete(role_id: UUID, db: Session = Depends(get_db)):
    role = crud.delete_role(db, role_id)
    return {"data": role, "message": "角色删除成功"}
