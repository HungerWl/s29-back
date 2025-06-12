from sqlalchemy.orm import Session
from app.post import models, schemas
from uuid import UUID
from fastapi import HTTPException


def create_post(db: Session, post_in: schemas.PostCreate):
    post = models.Post(**post_in.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def get_all_post(db: Session):
    return db.query(models.Post).order_by(models.Post.code.asc()).all()


def update_post(db: Session, post_id: UUID, post_in: schemas.PostUpdate):
    db_post = db.query(models.Post).filter(models.Post.id == str(post_id)).first()
    if not db_post:
        return None
    for key, value in post_in.model_dump(exclude_unset=True).items():
        setattr(db_post, key, value)
    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post(db: Session, post_id: UUID):
    post = db.query(models.Post).filter(models.Post.id == str(post_id)).first()
    if post:
        db.delete(post)
        db.commit()
    return post
