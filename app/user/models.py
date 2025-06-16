# 从核心模块导入Base
from core.database import Base
from sqlalchemy import Column, String, Boolean, ForeignKey
import uuid
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    # 外键关联部门（多对一）
    dept_id = Column(String(36), ForeignKey("dept.id"), index=True)
    # 外键关联岗位（多对一）
    post_id = Column(String(36), ForeignKey("post.id"), index=True)
    role_id = Column(String(36), ForeignKey("role.id"), index=True)
    # 关系字段（SQLAlchemy关系映射，非数据库字段）
    dept = relationship("Dept", back_populates="users")
    post = relationship("Post", back_populates="users")
    role = relationship("Role", back_populates="users")
