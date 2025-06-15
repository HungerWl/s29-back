from sqlalchemy.orm import Session
from starlette import status
from app.post import models, schemas
from uuid import UUID
from sqlalchemy.exc import IntegrityError
from core.exceptions import BusinessException


def get_post_by_name(db: Session, name: str):
    return db.query(models.Post).filter(models.Post.name == name).first()


def get_post_by_code(db: Session, code: str):
    return db.query(models.Post).filter(models.Post.code == code).first()


def create_post(db: Session, post_in: schemas.PostCreate):
    if get_post_by_name(db, post_in.name):
        raise BusinessException(
            entity="岗位名称",
            error_type="已存在",
        )
    if get_post_by_code(db, post_in.code):
        raise BusinessException(
            entity="岗位编码",
            error_type="已存在",
        )
    try:
        post = models.Post(**post_in.model_dump())
        db.add(post)
        db.commit()
        db.refresh(post)
        return post
    except IntegrityError as e:
        db.rollback()
        raise BusinessException(
            entity="department",
            error_type="database_error",
            details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def get_all_post(db: Session):
    return db.query(models.Post).order_by(models.Post.code.asc()).all()


def update_post(db: Session, post_id: UUID, post_in: schemas.PostUpdate):
    db_post = db.query(models.Post).filter(models.Post.id == str(post_id)).first()
    if not db_post:
        raise BusinessException(
            entity="岗位",
            error_type="不存在",
            status_code=status.HTTP_404_NOT_FOUND
        )
    try:
        for key, value in post_in.model_dump(exclude_unset=True).items():
            setattr(db_post, key, value)
        db.commit()
        db.refresh(db_post)
        return db_post
    except IntegrityError as e:
        db.rollback()
        raise BusinessException(
            entity="post",
            error_type="database_error",
            details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def delete_post(db: Session, post_id: UUID):
    try:
        post = db.query(models.Post).filter(models.Post.id == str(post_id)).first()
        if post:
            db.delete(post)
            db.commit()
        return post
    except IntegrityError as e:
        db.rollback()
        raise BusinessException(
            entity="post",
            error_type="delete_error",
            details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
