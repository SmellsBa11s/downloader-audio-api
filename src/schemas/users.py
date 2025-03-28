from pydantic import BaseModel


class UserInfo(BaseModel):
    id: int
    yandex_id: str
    first_name: str
    last_name: str
    email: str

class UpdateUserInfo(BaseModel):
    first_name: str
    last_name: str
    email: str

