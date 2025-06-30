import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

# 统一导入所有模型
from app.user import models as user_models
from app.post import models as post_models
from app.dept import models as dept_models
from app.menu import models as menu_models

# 统一导入所有路由
from app.dept.routers import dept_router
from app.post.routers import post_router
from app.role.routers import role_router
from app.user.routers import user_router
from app.menu.routers import menu_router

from core.exceptions import BusinessException, business_exception_handler
from core.exception_handlers import validation_exception_handler

app = FastAPI()

# 注册异常处理器
app.add_exception_handler(BusinessException, business_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# 注册路由
app.include_router(dept_router)
app.include_router(post_router)
app.include_router(role_router)
app.include_router(user_router)
app.include_router(menu_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
