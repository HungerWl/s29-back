from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.user import schemas, crud
from core.database import get_db
from typing import List, Optional
from core.exceptions import BusinessException
from core.schemas.base import BaseResponse
from uuid import UUID

user_router = APIRouter(prefix="/user", tags=["用户管理"])


@user_router.post(
    "/create",
    response_model=BaseResponse[schemas.UserOut],
    summary="创建用户",
    description="创建新用户"
)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        user = crud.create_user(db, user_in)
        return {"data": user, "message": "用户创建成功"}
    except BusinessException as e:
        raise e


@user_router.get(
    "/list",
    response_model=BaseResponse[List[schemas.UserOut]],
    summary="获取用户列表",
)
def list_all(
        dept_id: Optional[str] = None,  # 改为接受字符串类型
        db: Session = Depends(get_db)
):
    users_list = crud.get_all_user(db, dept_id)
    return {"data": users_list}


@user_router.delete(
    "/delete/{user_id}",
    response_model=BaseResponse[schemas.UserOut],
    summary="删除用户",
    description="永久删除指定用户",
    # responses={
    #     404: {"description": "用户不存在"},
    #     403: {"description": "禁止删除超级用户"},
    #     400: {"description": "无效请求"}
    # }
)
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    try:
        deleted_user = crud.delete_user(db, user_id)
        return {"data": deleted_user, "message": "用户删除成功"}
    except BusinessException as e:
        raise e


@user_router.put(
    "/update/{user_id}",
    response_model=BaseResponse[schemas.UserOut],
    summary="更新用户",
    description="更新用户信息",
    # responses={
    #     404: {"description": "用户不存在"},
    #     400: {"description": "数据验证失败"},
    #     409: {"description": "用户名/邮箱/手机号已存在"}
    # }
)
def update_user(
        user_id: UUID,
        user_update: schemas.UserUpdate,
        db: Session = Depends(get_db),
        # current_user: schemas.UserOut = Depends(get_current_active_user)  # 实际项目中需要权限验证
):
    try:
        updated_user = crud.update_user(db, user_id, user_update)
        return {"data": updated_user, "message": "用户更新成功"}
    except BusinessException as e:
        raise e
