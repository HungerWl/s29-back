# apps/post/models.py

from core.database import Base
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
import uuid


class Post(Base):
    __tablename__ = "post"  # 注意：表名为 post，保持与 ForeignKey("post.id") 一致

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False, unique=True, index=True)  # 岗位名称
    code = Column(String(50), unique=True, index=True, nullable=True)  # 岗位编码
    is_active = Column(Boolean, default=True, nullable=False)  # 岗位状态：启用/禁用
    remark = Column(String(255), nullable=True)  # 备注

    users = relationship("User", back_populates="post")
