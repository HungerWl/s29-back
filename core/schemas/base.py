# core/schemas/base.py
from pydantic import BaseModel
from typing import TypeVar, Optional, Generic
from datetime import datetime

T = TypeVar("T")


# 成功响应模型
class BaseResponse(BaseModel, Generic[T]):
    code: int = 200
    message: str = "success"
    data: Optional[T] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ErrorResponse(BaseModel, Generic[T]):
    """统一错误响应模型"""
    code: int  # HTTP状态码或自定义业务错误码
    message: str  # 错误概要信息
    details: Optional[str] = None  # 错误详情(可选)
    error_type: Optional[str] = None  # 错误类型(可选)
