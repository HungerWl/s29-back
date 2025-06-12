import uvicorn
from fastapi import FastAPI
from core.database import Base, engine
from app.user.routers import user
from app.user.models import User
from app.post.models import Post
from app.dept.models import Dept
from app.dept.routers import dept_router
from app.post.routers import post_router

app = FastAPI()

app.include_router(dept_router)
app.include_router(post_router)


# 在应用启动时创建数据库表
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
