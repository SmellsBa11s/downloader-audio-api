from datetime import datetime
from pydantic import BaseModel


class UserInfo(BaseModel):
    id: int
    yandex_id: str
    first_name: str
    last_name: str
    email: str
    is_active: bool
    is_supervisor: bool
    created_at: datetime
    updated_at: datetime


class UpdateUserInfo(BaseModel):
    first_name: str
    last_name: str
    email: str
