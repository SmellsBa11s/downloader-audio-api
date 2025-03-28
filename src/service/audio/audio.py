import os

from uuid import uuid4

from fastapi import Depends, HTTPException, UploadFile

from src.crud import AudioDAO
from src.models import User
from src.schemas import AudioResponse, AudioInfo
from src.schemas import AudioInfo
from src.service.audio import FileStorage, LocalFileStorage, FileValidator
from src.settings import settings


class AudioService:
    """Service for handling audio file operations.

    This service provides functionality for uploading, managing, and deleting audio files.
    It handles file storage, validation, and database operations.

    Attributes:
        _audio_dao (AudioDAO): Data access object for audio operations
        _storage (FileStorage): Storage service for file operations
        _media_dir (str): Directory for storing media files
    """

    def __init__(
        self,
        audio_dao: AudioDAO = Depends(),
        storage: FileStorage = Depends(LocalFileStorage),
    ):
        """Initialize the audio service.

        Args:
            audio_dao (AudioDAO): Data access object for audio operations
            storage (FileStorage): Storage service for file operations
        """
        self._audio_dao = audio_dao
        self._storage = storage
        self._media_dir = settings.MEDIA_DIR
        os.makedirs(self._media_dir, exist_ok=True)

    async def upload_audio(self, user: User, file: UploadFile, user_filename: str) -> AudioResponse:
        """Upload an audio file and save its information to the database.

        Args:
            user (User): The user uploading the file
            file (UploadFile): The audio file to upload
            user_filename (str): Name given to the file by the user

        Returns:
            AudioResponse: Information about the uploaded file

        Raises:
            HTTPException: 400 if file validation fails
        """
        FileValidator.validate_audio(file)

        file_extension = file.filename.split(".")[-1]
        unique_filename = f"user_{user.id}_{uuid4()}.{file_extension}"
        file_path = os.path.join(self._media_dir, unique_filename)

        content = await file.read()
        file_size = len(content)

        await self._storage.save_file(file, file_path, content)

        audio_info = AudioInfo(
            filename=unique_filename,
            user_filename=user_filename,
            user_id=user.id,
            path=file_path,
            size=file_size
        )
        await self._audio_dao.add(audio_info)

        return AudioResponse(
            filename=unique_filename,
            user_filename=user_filename,
            content_type=file.content_type,
            path=file_path,
            size=file_size,
        )

    async def delete_audio(
        self, audio_id: int, user: User, full_delete: bool = False
    ) -> None:
        """Delete an audio file and its information from the database.

        Args:
            audio_id (int): ID of the audio file to delete
            user (User): The user requesting the deletion
            full_delete (bool, optional): If True, permanently delete the file.
                If False, only mark it as deleted. Defaults to False.

        Raises:
            HTTPException:
                403 - If user doesn't have permission to delete the file
                404 - If audio file not found
        """
        audio = await self._audio_dao.find_one(id=audio_id, is_deleted=False)

        if (audio.user_id != user.id) and not (user.is_supervisor):
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to delete this audio file",
            )

        if full_delete:
            await self._storage.delete_file(audio.path)
            await self._audio_dao.delete(audio_id)
        else:
            await self._audio_dao.update(model_id=audio_id, is_deleted=True)
