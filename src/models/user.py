from sqlalchemy.orm import mapped_column, Mapped
from src.models.base import Base
from datetime import datetime


class User(Base):
    """SQLAlchemy model for users.

    This model represents users in the database with their authentication and profile information.

    Attributes:
        id (int): Primary key, auto-incrementing
        yandex_id (str): Yandex OAuth ID of the user
        first_name (str): User's first name
        last_name (str): User's last name
        email (str): User's email address (unique)
        is_active (bool): Whether the user account is active
        is_supervisor (bool): Whether the user has admin privileges
        created_at (datetime): Account creation timestamp
        updated_at (datetime): Last update timestamp
    """

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    yandex_id: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_supervisor: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )
