from datetime import datetime
from pydantic import BaseModel


class AudioResponse(BaseModel):
    filename: str
    content_type: str
    path: str
    size: int


class AudioInfo(BaseModel):
    filename: str
    user_id: int
    path: str
    size: int


class AudioFullInfo(AudioInfo):
    audio_id: int
    created_at: datetime
