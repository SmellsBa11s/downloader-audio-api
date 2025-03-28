from src.models.user import User
from src.crud.base import BaseDAO


class UserDAO(BaseDAO):
    """Data Access Object for users.

    This class provides CRUD operations for users in the database.
    Inherits all basic CRUD operations from BaseDAO.

    Attributes:
        model (User): SQLAlchemy model for users
    """

    model = User
