from src.models import AudioInfo
from src.crud.base import BaseDAO


class AudioDAO(BaseDAO):
    """Data Access Object for audio files.

    This class provides CRUD operations for audio files in the database.
    Inherits all basic CRUD operations from BaseDAO.

    Attributes:
        model (AudioInfo): SQLAlchemy model for audio files
    """

    model = AudioInfo
