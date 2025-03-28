from datetime import datetime
from pydantic import BaseModel


class AudioResponse(BaseModel):
    """Audio file response model.

    This model represents the audio file information for HTTP responses.

    Attributes:
        filename (str): Name of the audio file
        user_filename (str): Name given to the file by the user
        content_type (str): MIME type of the audio file
        path (str): Path to the audio file in storage
        size (int): Size of the audio file in bytes
    """

    filename: str
    user_filename: str
    content_type: str
    path: str
    size: int


class AudioInfo(BaseModel):
    """Basic audio file information model.

    This model represents the basic information about an audio file.

    Attributes:
        filename (str): Name of the audio file
        user_filename (str): Name given to the file by the user
        user_id (int): ID of the user who owns the file
        path (str): Path to the audio file in storage
        size (int): Size of the audio file in bytes
    """

    filename: str
    user_filename: str
    user_id: int
    path: str
    size: int


class AudioFullInfo(AudioInfo):
    """Complete audio file information model.

    This model extends AudioInfo with additional metadata about the audio file.

    Attributes:
        audio_id (int): Unique identifier of the audio file
        created_at (datetime): Timestamp when the file was created
    """

    audio_id: int
    is_deleted: bool
    created_at: datetime
