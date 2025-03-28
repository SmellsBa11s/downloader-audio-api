from abc import ABC, abstractmethod
import os
from fastapi import UploadFile


class FileStorage(ABC):
    """Abstract base class for file storage implementations.

    This class defines the interface for file storage operations.
    Concrete implementations must provide methods for saving and deleting files.

    Methods:
        save_file: Save a file to storage
        delete_file: Delete a file from storage
    """

    @abstractmethod
    async def save_file(
        self, file: UploadFile, file_path: str, content: bytes = None
    ) -> None:
        """Save a file to storage.

        Args:
            file (UploadFile): The file to save
            file_path (str): Path where the file should be saved
            content (bytes, optional): File content. If None, will be read from file.
        """
        pass

    @abstractmethod
    async def delete_file(self, file_path: str) -> None:
        """Delete a file from storage.

        Args:
            file_path (str): Path to the file to delete
        """
        pass


class LocalFileStorage(FileStorage):
    """Implementation of FileStorage for local file system.

    This class provides methods for saving and deleting files on the local file system.

    Methods:
        save_file: Save a file to local storage
        delete_file: Delete a file from local storage
    """

    async def save_file(
        self, file: UploadFile, file_path: str, content: bytes = None
    ) -> None:
        """Save a file to local storage.

        Args:
            file (UploadFile): The file to save
            file_path (str): Path where the file should be saved
            content (bytes, optional): File content. If None, will be read from file.
        """
        if content is None:
            content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

    async def delete_file(self, file_path: str) -> None:
        """Delete a file from local storage.

        Args:
            file_path (str): Path to the file to delete
        """
        if os.path.exists(file_path):
            os.remove(file_path)
