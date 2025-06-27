# 导入必要的模块和类
from core.database import Base  # 数据库基类，用于模型继承
from sqlalchemy import Column, String, Boolean  # SQLAlchemy字段类型
from sqlalchemy.orm import relationship  # 用于定义表关系
import uuid  # 用于生成UUID


# 定义Role角色模型类，继承自Base
class Role(Base):
    # 指定数据库表名
    __tablename__ = "roles"

    # 主键ID字段，使用UUID作为唯一标识符
    # String(36)因为UUID通常为36个字符长度
    # default使用lambda函数生成UUID并转为字符串
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False, index=True)
    
    # 角色名称字段
    # String(100)限制最大长度100字符
    # nullable=False表示不能为空
    # unique=True确保名称唯一
    # index=True创建索引提高查询效率
    name = Column(String(100), nullable=False, unique=True, index=True)

    # 权限键字段，用于标识角色权限
    # 同样要求唯一且非空
    permission_key = Column(String(100), unique=True, nullable=False)

    # 是否激活状态字段
    # Boolean类型，默认值为True(激活状态)
    # nullable=False表示不能为空
    is_active = Column(Boolean, default=True, nullable=False)

    # 备注字段
    # String(255)允许较长文本
    # nullable=True表示可以为空
    remark = Column(String(255), nullable=True)

    # 定义与User模型的关系
    # relationship创建一对多关系(一个角色可以对应多个用户)
    # back_populates="role"表示在User模型中也有对应的role关系字段
    users = relationship("User", back_populates="role")
