# apps/menu/schemas.py
from pydantic import BaseModel, Field, model_validator
from typing import Optional, List
from datetime import datetime
from core.schemas.base import BaseResponse
from pydantic import field_validator


# ✅ 1. 公共字段
class MenuBase(BaseModel):
    parent_id: Optional[int] = Field(None, description="上级菜单 ID")
    menu_type: str = Field(..., description="菜单类型，如 menu/button")
    menu_name: str = Field(..., max_length=50, description="菜单名称")
    icon: Optional[str] = Field(None, description="菜单图标")
    route_name: Optional[str] = Field(None, description="路由名称")
    route_path: Optional[str] = Field(None, description="路由地址")
    component: Optional[str] = Field(None, description="组件路径")
    permission: Optional[str] = Field(None, description="权限字符")
    route_params: Optional[str] = Field(None, description="路由参数（JSON 字符串）")
    cache: bool = Field(default=True, description="是否缓存")
    show_status: bool = Field(default=True, description="是否显示")
    menu_status: bool = Field(default=True, description="菜单状态")
    is_frame: bool = Field(default=False, description="是否外链")
    order_num: int = Field(default=0, description="排序")


# ✅ 2. 创建模型
class MenuCreate(MenuBase):
    
    @model_validator(mode='before')
    @classmethod
    def check_required_fields(cls, values):
        required_fields = ["menu_name", "menu_type"]
        for field in required_fields:
            value = values.get(field)
            if value is None or (isinstance(value, str) and not value.strip()):
                raise ValueError(f"{field} 不能为空或空字符串")
        return values


# ✅ 3. 更新模型
class MenuUpdate(MenuBase):
    pass


# ✅ 4. 响应模型（支持 ORM，含时间、ID、children）
class MenuOut(MenuBase):
    id: int = Field(..., description="菜单 ID")
    create_time: datetime = Field(..., description="创建时间")
    update_time: datetime = Field(..., description="更新时间")
    children: Optional[List["MenuOut"]] = None  # 用于递归树形结构

    class Config:
        from_attributes = True  # ✅ 推荐写法，替代 orm_mode


MenuOut.model_rebuild()
