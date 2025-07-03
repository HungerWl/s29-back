from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.user import schemas, crud
from core.database import get_db
from typing import List, Optional
from core.exceptions import BusinessException
from core.schemas.base import BaseResponse
from uuid import UUID
from fastapi.security import OAuth2PasswordRequestForm
from core.auth import create_access_token, get_current_user  # 添加此行导入
from pydantic import BaseModel

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


# 添加登录响应模型
class Token(BaseModel):
    access_token: str
    token_type: str
    user_info: schemas.UserOut


@user_router.post("/login", response_model=BaseResponse[Token], summary="用户登录")
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise BusinessException(
            entity="用户",
            error_type="认证失败",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    # 构建包含关联信息的用户数据
    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "nickname": user.nickname,
        "phone": user.phone,
        "gender": user.gender.value,
        "is_active": user.is_active,
        "is_superuser": user.is_superuser,
        "dept_id": user.dept_id,
        "role_id": user.role_id,
        "post_id": user.post_id,
        # 部门信息
        "dept_info": {
            "id": user.dept.id,
            "name": user.dept.name
        } if user.dept else None,
        # 角色信息
        "role_info": {
            "id": user.role.id,
            "name": user.role.name
        } if user.role else None,
        # 岗位信息
        "post_info": {
            "id": user.post.id,
            "name": user.post.name
        } if user.post else None
    }

    # 创建访问令牌
    access_token = create_access_token(data={"sub": user.username})
    return {
        "data": {
            "access_token": access_token,
            "token_type": "bearer",
            "user_info": user_data
        },
        "message": "登录成功"
    }


# 修改现有路由添加认证保护，例如:
@user_router.get(
    "/list",
    response_model=BaseResponse[List[schemas.UserOut]],
    summary="获取用户列表",
)
def list_all(
        dept_id: Optional[str] = None,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)  # 添加认证依赖
):
    # 解决未使用提示（如打印用户名）
    _ = current_user.username
    users_list = crud.get_all_user(db, dept_id)
    return {"data": users_list}


@user_router.post("/reset-password-by-info", response_model=BaseResponse, summary="通过账户信息重置密码")
def reset_password_by_information(
        request: schemas.PasswordResetByInfo,
        db: Session = Depends(get_db)
):
    success = crud.reset_password_by_info(
        db,
        username=request.username,
        email=request.email,
        phone=request.phone,
        new_password=request.new_password
    )
    if not success:
        raise BusinessException(
            entity="用户信息",
            error_type="账户名、邮箱或手机号不匹配",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    return {"message": "密码重置成功，请使用新密码登录"}
