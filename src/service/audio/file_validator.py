from fastapi import HTTPException, UploadFile, status


class FileValidator:
    """Класс для валидации файлов."""

    ALLOWED_EXTENSIONS = {"mp3", "wav", "ogg", "m4a", "flac"}
    MAX_FILE_SIZE = 50 * 1024 * 1024

    @classmethod
    def validate_audio(cls, file: UploadFile) -> None:
        """Проверяет файл на соответствие требованиям."""
        if not file.content_type.startswith("audio/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Разрешены только аудио файлы",
            )

        file_extension = file.filename.split(".")[-1].lower()
        if file_extension not in cls.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Неподдерживаемый формат файла. Разрешены: {', '.join(cls.ALLOWED_EXTENSIONS)}",
            )
