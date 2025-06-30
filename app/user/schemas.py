from pydantic import BaseModel, Field, model_validator
from typing import Optional
from uuid import UUID
from enum import Enum
from passlib.context import CryptContext


class GenderEnum(str, Enum):
    FEMALE = "0"
    MALE = "1"


class UserBase(BaseModel):
    username: str = Field(..., min_length=1, max_length=50, description="用户名")
    email: str = Field(..., description="邮箱")
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    phone: str = Field(..., min_length=11, max_length=20, description="手机号")
    gender: GenderEnum = Field(default=GenderEnum.MALE, description="性别")
    is_active: bool = Field(default=True, description="是否激活")
    remark: Optional[str] = Field(None, max_length=255, description="备注")
    password: str = Field(None, min_length=6, max_length=128, description="密码")


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=128, description="密码")
    dept_id: Optional[UUID] = Field(None, description="部门ID")
    role_id: Optional[UUID] = Field(None, description="角色ID")
    post_id: Optional[UUID] = Field(None, description="岗位ID")

    @model_validator(mode='before')
    @classmethod
    def check_required_fields(cls, values):
        required_fields = ["username", "email", "phone", "password"]
        for field in required_fields:
            value = values.get(field)
            if value is None or (isinstance(value, str) and not value.strip()):
                raise ValueError(f"{field} 不能为空或空字符串")
        return values


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=1, max_length=50, description="用户名")
    email: Optional[str] = Field(None, description="邮箱")
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    phone: Optional[str] = Field(None, min_length=11, max_length=20, description="手机号")
    gender: Optional[GenderEnum] = Field(None, description="性别")
    is_active: Optional[bool] = Field(None, description="是否激活")
    remark: Optional[str] = Field(None, max_length=255, description="备注")
    password: Optional[str] = Field(None, min_length=6, max_length=128, description="密码")
    dept_id: Optional[UUID] = Field(None, description="部门ID")
    role_id: Optional[UUID] = Field(None, description="角色ID")
    post_id: Optional[UUID] = Field(None, description="岗位ID")

    @model_validator(mode='before')
    @classmethod
    def check_required_fields(cls, values):
        required_fields = ["username", "email", "phone", "password"]
        for field in required_fields:
            value = values.get(field)
            if value is None or (isinstance(value, str) and not value.strip()):
                raise ValueError(f"{field} 不能为空或空字符串")
        return values


class UserOut(UserBase):
    id: UUID
    is_superuser: bool = Field(False, description="是否超级用户")
    dept_id: Optional[UUID] = Field(None, description="部门ID")
    role_id: Optional[UUID] = Field(None, description="角色ID")
    post_id: Optional[UUID] = Field(None, description="岗位ID")

    # 关联对象详情
    dept_info: Optional[dict] = Field(None, description="部门详情")
    role_info: Optional[dict] = Field(None, description="角色详情")
    post_info: Optional[dict] = Field(None, description="岗位详情")

    class Config:
        from_attributes = True
