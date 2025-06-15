from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict
from app.post import schemas, crud
from core.database import get_db
from uuid import UUID

post_router = APIRouter(prefix="/post", tags=["岗位管理"])


@post_router.post(
    "/",
    response_model=schemas.BaseResponse[schemas.PostInDB],
    summary="创建岗位",
    description="创建新岗位"
)
def create(dept_in: schemas.PostCreate, db: Session = Depends(get_db)):
    post = crud.create_post(db, dept_in)
    return {"data": post, "message": "岗位创建成功"}


@post_router.get(
    "/",
    response_model=schemas.BaseResponse[List[schemas.PostInDB]],
    summary="获取岗位列表",
)
def list_all(db: Session = Depends(get_db)):
    post = crud.get_all_post(db)
    return {"data": post}


@post_router.put(
    "/{post_id}",
    response_model=schemas.BaseResponse[schemas.PostInDB],
    summary="更新岗位",
    description="更新岗位信息"
)
def update(post_id: UUID, post_in: schemas.PostUpdate, db: Session = Depends(get_db)):
    post = crud.update_post(db, post_id, post_in)
    if not post:
        raise HTTPException(status_code=404, detail="岗位不存在")
    return {"data": post}


@post_router.delete(
    "/{dept_id}",
    response_model=schemas.BaseResponse[Dict],
    summary="删除部门"
)
def delete(dept_id: UUID, db: Session = Depends(get_db)):
    success = crud.delete_post(db, dept_id)
    if not success:
        raise HTTPException(status_code=404, detail="部门不存在")
    return {"message": "删除成功"}
