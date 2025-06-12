# utils/response.py

from typing import Any
from fastapi.responses import JSONResponse


def success(data: Any = None, message: str = "操作成功", code: int = 200):
    return JSONResponse(
        status_code=code,
        content={"code": code, "message": message, "data": data}
    )


def error(message: str = "操作失败", code: int = 400):
    return JSONResponse(
        status_code=code,
        content={"code": code, "message": message, "data": None}
    )
