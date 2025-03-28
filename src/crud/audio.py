from src.models import AudioInfo
from src.crud.base import BaseDAO


class AudioDAO(BaseDAO):
    model = AudioInfo
