from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship, backref  # 添加backref导入
from core.database import Base


class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True)

    parent_id = Column(Integer, ForeignKey("menus.id", ondelete="CASCADE"), nullable=True, index=True,
                       comment="上级菜单ID，空表示顶级菜单")

    menu_type = Column(String(20), nullable=False, comment="菜单类型(menu/button)")
    menu_name = Column(String(50), nullable=False, comment="菜单名称")
    icon = Column(String(100), nullable=True, comment="菜单图标")
    route_name = Column(String(50), nullable=True, comment="路由名称")
    route_path = Column(String(200), nullable=True, comment="路由地址")
    component = Column(String(200), nullable=True, comment="组件路径")
    permission = Column(String(100), nullable=True, comment="权限字符")
    route_params = Column(Text, nullable=True, comment="路由参数，JSON字符串格式建议")

    cache = Column(Boolean, nullable=False, default=True, comment="是否缓存")
    show_status = Column(Boolean, nullable=False, default=True, comment="显示状态")
    menu_status = Column(Boolean, nullable=False, default=True, comment="菜单状态")
    is_frame = Column(Boolean, nullable=False, default=False, comment="是否外链")

    order_num = Column(Integer, nullable=False, default=0, comment="排序")

    create_time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    update_time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'), onupdate=text('now()'))

    # 关系字段，修改关系字段，添加子菜单排序
    parent = relationship("Menu", remote_side="Menu.id", backref=backref("children", order_by="Menu.order_num"))
