from fastapi import HTTPException, UploadFile, status


class FileValidator:
    """Class for validating uploaded files.

    This class provides validation methods for different types of files,
    ensuring they meet specific requirements for format and size.

    Attributes:
        ALLOWED_EXTENSIONS (set[str]): Set of allowed file extensions
        MAX_FILE_SIZE (int): Maximum allowed file size in bytes
    """

    ALLOWED_EXTENSIONS = {"mp3", "wav", "ogg", "m4a", "flac"}
    MAX_FILE_SIZE = 50 * 1024 * 1024

    @classmethod
    def validate_audio(cls, file: UploadFile) -> None:
        """Validate an audio file.

        Checks if the file is an audio file and has an allowed extension.

        Args:
            file (UploadFile): The file to validate

        Raises:
            HTTPException: 400 if file is not an audio file or has unsupported format
        """
        if not file.content_type.startswith("audio/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only audio files are allowed",
            )

        file_extension = file.filename.split(".")[-1].lower()
        if file_extension not in cls.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file format. Allowed formats: {', '.join(cls.ALLOWED_EXTENSIONS)}",
            )
