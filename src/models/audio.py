from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from src.models.base import Base
from datetime import datetime


class AudioInfo(Base):
    """SQLAlchemy model for audio files.

    This model represents audio files in the database with their metadata.

    Attributes:
        id (int): Primary key, auto-incrementing
        filename (str): Name of the audio file
        path (str): Path to the audio file in storage
        size (int): Size of the audio file in bytes
        user_id (int): Foreign key to the user who owns the file
        is_deleted (bool): Flag indicating if the file is deleted
        created_at (datetime): Timestamp when the file was created
    """

    __tablename__ = "audio_info"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    filename: Mapped[str] = mapped_column(nullable=False)
    path: Mapped[str] = mapped_column(nullable=False)
    size: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    is_deleted: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
