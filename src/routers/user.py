from fastapi import APIRouter, Depends, File, UploadFile

from src.core.dependencies import get_current_user
from src.models import User
from src.schemas import AudioResponse
from src.service import AudioService

router = APIRouter()


@router.post("/upload-audio/")
async def upload_user_audio(
    file_name: str,
    user: User = Depends(get_current_user),
    file: UploadFile = File(...),
    audio_service: AudioService = Depends(AudioService),
) -> AudioResponse:
    """Upload an audio file.

    This endpoint allows authenticated users to upload audio files.
    The file is validated, stored, and its information is saved in the database.

    Args:
        file_name (str): Name given to the file by the user
        user (User): Current authenticated user
        file (UploadFile): The audio file to upload
        audio_service (AudioService): Service for handling audio operations

    Returns:
        AudioResponse: Information about the uploaded file

    Raises:
        HTTPException: 400 if file validation fails
    """
    result = await audio_service.upload_audio(user=user, file=file, user_filename=file_name)
    return result


@router.delete("/delete-audio/")
async def delete_user_audio(
    audio_id: int,
    full_delete: bool = False,
    audio_service: AudioService = Depends(AudioService),
    user: User = Depends(get_current_user),
) -> bool:
    """Delete an audio file.

    This endpoint allows users to delete their own audio files.
    Users can either mark the file as deleted or permanently remove it.

    Args:
        audio_id (int): ID of the audio file to delete
        full_delete (bool, optional): If True, permanently delete the file.
            If False, only mark it as deleted. Defaults to False.
        audio_service (AudioService): Service for handling audio operations
        user (User): Current authenticated user

    Returns:
        bool: True if deletion was successful

    Raises:
        HTTPException:
            403 - If user doesn't have permission to delete the file
            404 - If audio file not found
    """
    await audio_service.delete_audio(
        audio_id=audio_id, full_delete=full_delete, user=user
    )
    return True
