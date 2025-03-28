from datetime import datetime
from pydantic import BaseModel


class UserInfo(BaseModel):
    """User information model.

    This model represents the complete user information including personal details
    and account status.

    Attributes:
        id (int): Unique identifier of the user
        yandex_id (str): Yandex OAuth ID of the user
        first_name (str): User's first name
        last_name (str): User's last name
        email (str): User's email address
        is_active (bool): Whether the user account is active
        is_supervisor (bool): Whether the user has admin privileges
        created_at (datetime): Account creation timestamp
        updated_at (datetime): Last update timestamp
    """

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
    """User information update model.

    This model represents the fields that can be updated for a user.

    Attributes:
        first_name (str): User's first name
        last_name (str): User's last name
        email (str): User's email address
    """

    first_name: str
    last_name: str
    email: str
