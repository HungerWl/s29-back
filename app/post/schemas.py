# apps/post/schemas.py
from pydantic import BaseModel, Field
from typing import Optional, TypeVar
from uuid import UUID
from core.schemas.base import BaseResponse, ErrorResponse  # 引入公共模型

T = TypeVar('T')


class PostBase(BaseModel):
    name: str = Field(..., max_length=100, description="岗位名称")
    code: Optional[str] = Field(None, max_length=50, description="岗位编码")
    is_active: bool = Field(True, description="是否启用")
    remark: Optional[str] = Field(None, max_length=255, description="备注")


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100, description="岗位名称")
    code: Optional[str] = Field(None, max_length=50, description="岗位编码")
    is_active: Optional[bool] = Field(None, description="是否启用")
    remark: Optional[str] = Field(None, max_length=255, description="备注")


class PostInDB(PostBase):
    id: UUID

    class Config:
        from_attributes = True
        json_encoders = {
            UUID: lambda v: str(v)
        }
