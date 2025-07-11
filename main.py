import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

# 统一导入所有模型
from app.user import models as user_models
from app.post import models as post_models
from app.dept import models as dept_models
from app.menu import models as menu_models
from app.document import models as document_models

# 统一导入所有路由
from app.dept.routers import dept_router
from app.post.routers import post_router
from app.role.routers import role_router
from app.user.routers import user_router
from app.menu.routers import menu_router

from core.exceptions import BusinessException, business_exception_handler
from core.exception_handlers import validation_exception_handler

app = FastAPI()

# 添加CORS中间件（如果需要）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应指定具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
