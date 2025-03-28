from abc import ABC, abstractmethod
import os
from fastapi import UploadFile


class FileStorage(ABC):
    """Абстрактный класс для хранения файлов."""

    @abstractmethod
    async def save_file(
        self, file: UploadFile, file_path: str, content: bytes = None
    ) -> None:
        """Сохраняет файл."""
        pass

    @abstractmethod
    async def delete_file(self, file_path: str) -> None:
        """Удаляет файл."""
        pass


class LocalFileStorage(FileStorage):
    """Класс для локального хранения файлов."""

    async def save_file(
        self, file: UploadFile, file_path: str, content: bytes = None
    ) -> None:
        """Сохраняет файл локально."""
        if content is None:
            content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

    async def delete_file(self, file_path: str) -> None:
        """Удаляет файл локально."""
        if os.path.exists(file_path):
            os.remove(file_path)
