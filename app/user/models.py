from core.database import Base
from sqlalchemy import Column, String, Boolean, ForeignKey
import uuid
from sqlalchemy.orm import relationship
from enum import Enum
from sqlalchemy import Enum as SQLEnum


class GenderEnum(str, Enum):
    FEMALE = "0"
    MALE = "1"


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    gender = Column(SQLEnum(GenderEnum), default=GenderEnum.MALE, nullable=False)
    phone = Column(String(20), unique=True, index=True, nullable=False)

    # 可选字段
    nickname = Column(String(50), nullable=True)
    remark = Column(String(255), nullable=True)

    # 外键关系
    dept_id = Column(String(36), ForeignKey("depts.id"), nullable=True)
    role_id = Column(String(36), ForeignKey("roles.id"), nullable=True)
    post_id = Column(String(36), ForeignKey("posts.id"), nullable=True)

    # 关系字段
    dept = relationship("Dept", back_populates="users")
    post = relationship("Post", back_populates="users")
    role = relationship("Role", back_populates="users")
