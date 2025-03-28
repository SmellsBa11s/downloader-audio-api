from abc import ABC, abstractmethod
from fastapi import HTTPException, status
from fastapi.responses import FileResponse
from src.settings import settings
import os


class FileStorage(ABC):
    """Abstract base class for file storage operations.

    This class defines the interface for file storage operations,
    including saving, retrieving, and deleting files.

    Methods:
        save_file: Save a file to storage
        get_file: Retrieve a file from storage
        delete_file: Delete a file from storage
    """

    @abstractmethod
    async def save_file(self, file: bytes, file_path: str) -> None:
        """Save a file to storage.

        Args:
            file (bytes): File content to save
            file_path (str): Path where to save the file

        Raises:
            HTTPException: 500 if file saving fails
        """
        pass

    @abstractmethod
    async def get_file(self, file_path: str) -> FileResponse:
        """Retrieve a file from storage.

        Args:
            file_path (str): Path to the file

        Returns:
            FileResponse: The requested file

        Raises:
            HTTPException: 404 if file not found
        """
        pass

    @abstractmethod
    async def delete_file(self, file_path: str) -> None:
        """Delete a file from storage.

        Args:
            file_path (str): Path to the file to delete

        Raises:
            HTTPException: 500 if file deletion fails
        """
        pass


class LocalFileStorage(FileStorage):
    """Local file system storage implementation.

    This class implements file storage operations using the local file system.
    Files are stored in the directory specified by settings.MEDIA_DIR.

    Attributes:
        media_dir (str): Directory for storing media files
    """

    def __init__(self):
        self.media_dir = settings.MEDIA_DIR

    async def save_file(self, file: bytes, file_path: str) -> None:
        """Save a file to local storage.

        Args:
            file (bytes): File content to save
            file_path (str): Path where to save the file

        Raises:
            HTTPException: 500 if file saving fails
        """
        try:
            with open(file_path, "wb") as f:
                f.write(file)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to save file: {str(e)}",
            )

    async def get_file(self, file_path: str) -> FileResponse:
        """Retrieve a file from local storage.

        Args:
            file_path (str): Path to the file

        Returns:
            FileResponse: The requested file

        Raises:
            HTTPException: 404 if file not found
        """
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found",
            )
        return FileResponse(file_path)

    async def delete_file(self, file_path: str) -> None:
        """Delete a file from local storage.

        Args:
            file_path (str): Path to the file to delete

        Raises:
            HTTPException: 500 if file deletion fails
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete file: {str(e)}",
            )
