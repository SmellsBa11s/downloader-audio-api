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
    """Сервис для работы с аудио файлами."""

    def __init__(
        self,
        audio_dao: AudioDAO = Depends(),
        storage: FileStorage = Depends(LocalFileStorage),
    ):
        self._audio_dao = audio_dao
        self._storage = storage
        self._media_dir = settings.MEDIA_DIR
        os.makedirs(self._media_dir, exist_ok=True)

    async def upload_audio(self, user: User, file: UploadFile) -> AudioResponse:
        """Загружает аудио файл и сохраняет информацию в БД."""
        FileValidator.validate_audio(file)

        file_extension = file.filename.split(".")[-1]
        unique_filename = f"user_{user.id}_{uuid4()}.{file_extension}"
        file_path = os.path.join(self._media_dir, unique_filename)

        content = await file.read()
        file_size = len(content)

        await self._storage.save_file(file, file_path, content)

        audio_info = AudioInfo(
            filename=unique_filename, user_id=user.id, path=file_path, size=file_size
        )
        await self._audio_dao.add(audio_info)

        return AudioResponse(
            filename=unique_filename,
            content_type=file.content_type,
            path=file_path,
            size=file_size,
        )

    async def delete_audio(
        self, audio_id: int, user: User, full_delete: bool = False
    ) -> None:
        """Удаляет аудио файл и его информацию из БД."""
        audio = await self._audio_dao.find_one(id=audio_id, is_deleted=False)

        if (audio.user_id != user.id) and not (user.is_supervisor):
            raise HTTPException(
                status_code=403,
                detail="У вас недостаточно прав для удаления этого аудио файла",
            )

        if full_delete:
            await self._storage.delete_file(audio.path)
            await self._audio_dao.delete(audio_id)
        else:
            await self._audio_dao.update(model_id=audio_id, is_deleted=True)
