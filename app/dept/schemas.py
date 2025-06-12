# apps/dept/schemas.py

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

# DeptOut.model_rebuild()
