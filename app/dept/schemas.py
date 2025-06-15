# apps/dept/schemas.py
from pydantic import BaseModel, Field
from typing import Optional, TypeVar
from uuid import UUID
from core.schemas.base import BaseResponse, ErrorResponse  # 引入公共模型

T = TypeVar('T')


class DeptBase(BaseModel):
    name: str = Field(..., max_length=100)
    code: Optional[str] = Field(None, max_length=50)
    leader: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = None
    is_active: Optional[bool] = True
    remark: Optional[str] = Field(None, max_length=255)
    parent_id: Optional[UUID] = None


class DeptCreate(DeptBase):
    pass


class DeptUpdate(DeptBase):
    pass


class DeptOut(DeptBase):
    id: UUID

    class Config:
        from_attributes = True
        json_encoders = {
            UUID: lambda v: str(v)
        }
