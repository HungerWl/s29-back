from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.dept import schemas, crud
from core.database import get_db
from uuid import UUID

dept_router = APIRouter(prefix="/dept", tags=["部门管理"])


@dept_router.post(
    "/",
    response_model=schemas.BaseResponse[schemas.DeptOut],
    summary="创建部门",
    description="创建新部门"
)
def create(dept_in: schemas.DeptCreate, db: Session = Depends(get_db)):
    try:
        dept = crud.create_dept(db, dept_in)
        return {"data": dept}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@dept_router.get(
    "/",
    response_model=schemas.BaseResponse[List[schemas.DeptOut]],
    summary="获取部门列表",
)
def list_all(db: Session = Depends(get_db)):
    depths = crud.get_all_dept(db)
    return {"data": depths}


@dept_router.put(
    "/{dept_id}",
    response_model=schemas.BaseResponse[schemas.DeptOut],
    summary="更新部门",
    description="更新部门信息"
)
def update(dept_id: UUID, dept_in: schemas.DeptUpdate, db: Session = Depends(get_db)):
    dept = crud.update_dept(db, dept_id, dept_in)
    if not dept:
        raise HTTPException(status_code=404, detail="部门不存在")
    return {"data": dept}


@dept_router.delete(
    "/{dept_id}",
    response_model=schemas.BaseResponse[None],
    summary="删除部门"
)
def delete(dept_id: UUID, db: Session = Depends(get_db)):
    success = crud.delete_dept(db, dept_id)
    if not success:
        raise HTTPException(status_code=404, detail="部门不存在")
    return {"message": "删除成功"}
