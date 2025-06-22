from sqlalchemy.orm import Session, selectinload
from app.user import schemas
from app.user import models as user_models
from app.dept import models as dept_models  # 部门模型
from uuid import UUID
from core.exceptions import BusinessException
from fastapi import status
from sqlalchemy.exc import IntegrityError
from typing import Optional, Union  # 新增Union导入


def get_user_by_username(db: Session, username: str):
    return db.query(user_models.User).filter(user_models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(user_models.User).filter(user_models.User.email == email).first()


def get_user_by_phone(db: Session, phone: str):
    return db.query(user_models.User).filter(user_models.User.phone == phone).first()


def get_dept_and_children_ids(db: Session, dept_id: str) -> list[str]:
    """获取部门及其所有子部门的ID列表"""
    dept = db.query(dept_models.Dept).filter(dept_models.Dept.id == dept_id).first()
    if not dept:
        return []

    dept_ids = [dept_id]

    # 递归获取所有子部门ID
    def get_children_ids(parent_id: str):
        children = db.query(dept_models.Dept).filter(dept_models.Dept.parent_id == parent_id).all()
        for child in children:
            dept_ids.append(str(child.id))
            get_children_ids(str(child.id))

    get_children_ids(dept_id)
    return dept_ids


def create_user(db: Session, user_in: schemas.UserCreate):
    # 检查用户名是否已存在
    if get_user_by_username(db, user_in.username):
        raise BusinessException(
            entity="用户名称",
            error_type="已存在",
            status_code=status.HTTP_400_BAD_REQUEST
        )

    # 检查邮箱是否已存在
    if get_user_by_email(db, user_in.email):
        raise BusinessException(
            entity="邮箱",
            error_type="已存在",
            status_code=status.HTTP_400_BAD_REQUEST
        )

    # 检查手机号是否已存在
    if get_user_by_phone(db, user_in.phone):
        raise BusinessException(
            entity="手机号",
            error_type="已存在",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    try:
        db_user = user_models.User(
            username=user_in.username,
            email=user_in.email,
            phone=user_in.phone,
            gender=user_in.gender,
            is_active=user_in.is_active,
            nickname=user_in.nickname,
            remark=user_in.remark,
            dept_id=str(user_in.dept_id) if user_in.dept_id else None,
            role_id=str(user_in.role_id) if user_in.role_id else None,
            post_id=str(user_in.post_id) if user_in.post_id else None,
            password=user_in.password  # 实际项目中应该使用密码哈希
        )

        # 添加到数据库
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        db.rollback()
        raise BusinessException(
            entity="user",
            error_type="database_error",
            details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def get_all_user(db: Session, dept_id: Optional[Union[UUID, str]] = None):
    query = db.query(user_models.User).options(
        selectinload(user_models.User.dept),
        selectinload(user_models.User.role),
        selectinload(user_models.User.post)
    )

    # 只有当 dept_id 是有效的 UUID 字符串时才进行筛选
    if dept_id and dept_id != "null" and dept_id != "":
        try:
            # 确保 dept_id 是有效的 UUID
            valid_dept_id = str(UUID(str(dept_id)))
            # 获取部门及其所有子部门的ID
            dept_ids = get_dept_and_children_ids(db, valid_dept_id)
            query = query.filter(user_models.User.dept_id.in_(dept_ids))
        except ValueError:
            raise BusinessException(
                entity="部门ID",
                error_type="格式无效",
                status_code=status.HTTP_400_BAD_REQUEST
            )

    users = query.order_by(user_models.User.username.asc()).all()

    # 转换结果为字典并添加关联信息
    result = []
    for user in users:
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "nickname": user.nickname,
            "phone": user.phone,
            "gender": user.gender.value,  # 转换为字符串值
            "is_active": user.is_active,
            "remark": user.remark,
            "dept_id": user.dept_id,
            "role_id": user.role_id,
            "password": user.password,
            "post_id": user.post_id,
            "dept_info": {
                "id": user.dept.id,
                "name": user.dept.name
            } if user.dept else None,
            "role_info": {
                "id": user.role.id,
                "name": user.role.name
            } if user.role else None,
            "post_info": {
                "id": user.post.id,
                "name": user.post.name
            } if user.post else None
        }
        result.append(user_data)

    return result


def delete_user(db: Session, user_id: UUID):
    # 获取要删除的部门
    db_user = db.query(user_models.User).filter(user_models.User.id == str(user_id)).first()

    # 检查用户是否存在
    if not db_user:
        raise BusinessException(
            entity="用户",
            error_type="不存在",
            status_code=status.HTTP_404_NOT_FOUND
        )

    # 禁止删除超级用户
    if db_user.is_superuser:
        raise BusinessException(
            entity="用户",
            error_type="禁止删除超级用户",
            status_code=status.HTTP_403_FORBIDDEN
        )

    try:
        # 执行删除操作
        db.delete(db_user)
        db.commit()
        return db_user
    except IntegrityError as e:
        db.rollback()
        # 处理可能的关联约束错误
        raise BusinessException(
            entity="用户",
            error_type="删除失败",
            details=str(e),
            status_code=status.HTTP_400_BAD_REQUEST
        )


def update_user(db: Session, user_id: UUID, user_update: schemas.UserUpdate):
    db_user = db.query(user_models.User).filter(user_models.User.id == str(user_id)).first()

    if not db_user:
        raise BusinessException(
            entity="用户",
            error_type="不存在",
            status_code=status.HTTP_404_NOT_FOUND
        )

    # 检查用户名是否已存在（且不是当前用户）
    if user_update.username and user_update.username != db_user.username:
        if get_user_by_username(db, user_update.username):
            raise BusinessException(
                entity="用户名",
                error_type="已存在",
                status_code=status.HTTP_409_CONFLICT
            )

    # 检查邮箱是否已存在（且不是当前用户）
    if user_update.email and user_update.email != db_user.email:
        if get_user_by_email(db, user_update.email):
            raise BusinessException(
                entity="邮箱",
                error_type="已存在",
                status_code=status.HTTP_409_CONFLICT
            )

    # 检查手机号是否已存在（且不是当前用户）
    if user_update.phone and user_update.phone != db_user.phone:
        if get_user_by_phone(db, user_update.phone):
            raise BusinessException(
                entity="手机号",
                error_type="已存在",
                status_code=status.HTTP_409_CONFLICT
            )

    try:
        # 更新基本字段
        update_data = user_update.model_dump(exclude_unset=True, exclude={"password"})
        for field, value in update_data.items():
            setattr(db_user, field, value)

        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        db.rollback()
        raise BusinessException(
            entity="用户",
            error_type="更新失败",
            details=str(e),
            status_code=status.HTTP_400_BAD_REQUEST
        )
