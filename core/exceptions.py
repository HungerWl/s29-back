from fastapi import status, Request
from typing import Optional, Union, Dict, List, Any
from fastapi.responses import JSONResponse
from fastapi import HTTPException


class BusinessException(Exception):
    """通用业务异常基类（无detail包装版）"""

    def __init__(
            self,
            entity: str,  # 实体类型，如"dept", "post"
            error_type: str,  # 错误类型，如"not_found", "exists"
            details: Optional[Union[str, List[Dict[str, Any]]]] = None,  # 支持字符串或结构化数据
            status_code: int = status.HTTP_400_BAD_REQUEST
    ):
        # 预定义的错误类型映射表
        error_templates = {
            "not_found": "{entity} with ID {details} does not exist",
            "exists": "{entity} {details} already exists",
            "in_use": "{entity} is in use by {details}"
        }

        self.entity = entity
        self.error_type = error_type
        self.status_code = status_code
        self.details = details or ""

        # 自动生成message
        _translation = str.maketrans('_', ' ')
        self.message = f"{entity.translate(_translation).title()}_{error_type.translate(_translation).title()}"

        # 自动生成details（如果未提供）
        if not details and error_type in error_templates:
            self.details = error_templates[error_type].format(
                entity=entity.replace('_', ' '),
                details=details or ""
            )

    def to_http_exception(self):
        """转换为FastAPI的HTTPException（扁平化结构）"""
        return HTTPException(
            status_code=self.status_code,
            detail=self.to_dict()  # 直接返回字典，不再嵌套detail
        )

    def to_dict(self):
        """转换为字典格式（用于响应）"""
        return {
            "code": self.status_code,
            "message": self.message,
            "details": self.details,
            "entity": self.entity,
            "error_type": self.error_type
        }


async def business_exception_handler(request: Request, exc: BusinessException):
    """全局业务异常处理器（扁平化结构）"""
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict()  # 直接使用转换后的字典
    )
