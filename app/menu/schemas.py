from typing import Optional
from datetime import datetime
from pydantic import BaseModel, model_validator


class MenuBase(BaseModel):
    parent_id: Optional[int] = None
    menu_type: str = "menu"
    menu_name: str
    icon: Optional[str] = None
    route_name: Optional[str] = None
    route_path: Optional[str] = None
    component: Optional[str] = None
    permission: Optional[str] = None
    route_params: Optional[str] = None
    cache: bool = True
    show_status: bool = True
    menu_status: bool = True
    is_frame: bool = False
    order: int = 0


class MenuCreate(MenuBase):
    @model_validator(mode='before')
    @classmethod
    def check_required_fields(cls, values):
        required_fields = ["menu_type", "menu_name", "route_path", "order"]
        for field in required_fields:
            value = values.get(field)
            if value is None or (isinstance(value, str) and not value.strip()):
                raise ValueError(f"{field} 不能为空或空字符串")
        return values


class MenuUpdate(MenuBase):
    parent_id: Optional[int] = None
    menu_type: Optional[str] = None
    menu_name: Optional[str] = None
    icon: Optional[str] = None
    route_name: Optional[str] = None
    route_path: Optional[str] = None
    component: Optional[str] = None
    permission: Optional[str] = None
    route_params: Optional[str] = None
    cache: Optional[bool] = None
    show_status: Optional[bool] = None
    menu_status: Optional[bool] = None
    is_frame: Optional[bool] = None
    order: Optional[int] = None

    @model_validator(mode='before')
    @classmethod
    def check_required_fields(cls, values):
        required_fields = ["menu_type", "menu_name", "route_path", "order"]
        for field in required_fields:
            value = values.get(field)
            if value is None or (isinstance(value, str) and not value.strip()):
                raise ValueError(f"{field} 不能为空或空字符串")
        return values


class MenuInDB(MenuBase):
    id: int
    create_time: datetime
    update_time: datetime

    class Config:
        from_attributes = True
