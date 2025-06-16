# apps/role/schemas.py
from pydantic import BaseModel, Field
from typing import Optional, TypeVar
from uuid import UUID
from core.schemas.base import BaseResponse, ErrorResponse  # 引入公共模型

T = TypeVar('T')


class RoleBase(BaseModel):
    name: Optional[str] = Field(None, max_length=100, description="角色名称")
    permission_key: str = Field(min_length=3, max_length=100, description="权限字符")
    is_active: bool = Field(True, description="是否启用")
    remark: Optional[str] = Field(None, max_length=255, description="备注")


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100, description="角色名称")
    permission_key: Optional[str] = Field(None, min_length=3, max_length=100, description="权限字符")
    is_active: Optional[bool] = Field(None, description="是否启用")
    remark: Optional[str] = Field(None, max_length=255, description="备注")


class RoleInDB(RoleBase):
    id: UUID

    class Config:
        from_attributes = True
        json_encoders = {
            UUID: lambda v: str(v)
        }
