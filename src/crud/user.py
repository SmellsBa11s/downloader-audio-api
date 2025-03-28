from src.models.user import User
from src.crud.base import BaseDAO


class UserDAO(BaseDAO):
    model = User
