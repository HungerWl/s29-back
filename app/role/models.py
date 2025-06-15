# apps/role/models.py

from core.database import Base
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
import uuid


class Role(Base):
    __tablename__ = "role"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False, unique=True, index=True)
    permission_key = Column(String(100), unique=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    remark = Column(String(255), nullable=True)  # 备注

    users = relationship("User", back_populates="role")
