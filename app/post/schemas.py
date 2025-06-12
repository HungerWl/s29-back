# apps/post/schemas.py
from pydantic import BaseModel, Field
from typing import Optional, List, Generic, TypeVar
from uuid import UUID
from pydantic.generics import GenericModel

T = TypeVar('T')


class BaseResponse(BaseModel, Generic[T]):
    code: int = 200
    message: str = "success"
    data: Optional[T] = None


class ErrorResponse(BaseModel, Generic[T]):
    code: int
    message: str
    detail: Optional[str] = None


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
