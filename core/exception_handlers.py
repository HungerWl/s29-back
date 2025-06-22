from fastapi.exceptions import RequestValidationError
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from core.exceptions import BusinessException


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(request, exc)
    errors = exc.errors()
    custom_messages = []

    for error in errors:
        # 获取字段位置 (loc)
        field = ".".join(str(loc) for loc in error["loc"] if loc != "body")

        # 处理错误消息
        msg = error.get("msg", "Invalid value")

        if msg.startswith("Value error, "):
            msg = msg[13:]

        # 添加字段和错误信息
        custom_messages.append(f"{msg}")
    # 从 URL 中推测模块实体名
    path_parts = request.url.path.strip("/").split("/")
    entity = path_parts[0] if path_parts else "system"

    # 构建自定义业务异常
    biz_exc = BusinessException(
        entity=entity,
        error_type="validation_error",
        details="; ".join(custom_messages),
        status_code=HTTP_422_UNPROCESSABLE_ENTITY
    )

    return JSONResponse(
        status_code=biz_exc.status_code,
        content=biz_exc.to_dict()
    )
