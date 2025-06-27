# apps/dept/models.py

from core.database import Base
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
import uuid


class Dept(Base):
    __tablename__ = "depts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)

    name = Column(String(100), nullable=False, unique=True, index=True)  # 部门名称
    code = Column(String(50), unique=True, index=True, nullable=True)  # 部门编码
    leader = Column(String(50), nullable=True)  # 负责人
    phone = Column(String(20), nullable=True)  # 联系电话
    email = Column(String(100), nullable=True)  # 联系邮箱
    is_active = Column(Boolean, default=True, nullable=False)  # 状态，启用/禁用
    remark = Column(String(255), nullable=True)  # 备注说明

    parent_id = Column(String(36), ForeignKey("depts.id", ondelete="CASCADE"), nullable=True)  # 上级部门ID

    # 关系映射
    users = relationship("User", back_populates="dept")

    # 自关联关系，children表示下属部门列表，parent表示上级部门
    children = relationship("Dept", backref="parent", remote_side="Dept.id")  # ✅ 推荐这样写，字符串引用字段名
