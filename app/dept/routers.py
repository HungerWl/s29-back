from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from app.dept import schemas, crud
from core.database import get_db
from uuid import UUID

dept_router = APIRouter(prefix="/dept", tags=["部门管理"])


@dept_router.post(
    "/create",
    response_model=schemas.BaseResponse[schemas.DeptOut],
    summary="创建部门",
    description="创建新部门"
)
def create(dept_in: schemas.DeptCreate, db: Session = Depends(get_db)):
    dept = crud.create_dept(db, dept_in)
    return {"data": dept, "message": "部门创建成功"}


@dept_router.get(
    "/list",
    response_model=schemas.BaseResponse[List[schemas.DeptOut]],
    summary="获取部门列表",
)
def list_all(db: Session = Depends(get_db)):
    depts = crud.get_all_dept(db)
    return {"data": depts}


@dept_router.put(
    "/update/{dept_id}",
    response_model=schemas.BaseResponse[schemas.DeptOut],
    summary="更新部门",
    description="更新部门信息"
)
def update(dept_id: UUID, dept_in: schemas.DeptUpdate, db: Session = Depends(get_db)):
    dept = crud.update_dept(db, dept_id, dept_in)
    return {"data": dept, "message": "部门更新成功"}


@dept_router.delete(
    "/delete/{dept_id}",
    response_model=schemas.BaseResponse[None],
    summary="删除部门"
)
def delete(dept_id: UUID, db: Session = Depends(get_db)):
    success = crud.delete_dept(db, dept_id)
    if not success:
        raise HTTPException(status_code=404, detail="部门不存在")
    return {"message": "删除成功"}
