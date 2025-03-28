from src.crud.base import BaseDAO
from src.models import User


class UserDAO(BaseDAO):
    model = User
