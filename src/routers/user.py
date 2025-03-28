from fastapi import APIRouter, Depends, File, UploadFile

from src.core.dependencies import get_current_user
from src.models import User
from src.schemas import AudioResponse
from src.service import AudioService

router = APIRouter()


@router.post("/upload-audio/")
async def upload_user_audio(
    user: User = Depends(get_current_user),
    file: UploadFile = File(...),
    audio_service: AudioService = Depends(AudioService),
) -> AudioResponse:
    result = await audio_service.upload_audio(user, file)
    return result


@router.delete("/delete-audio/")
async def delete_user_audio(
    audio_id: int,
    full_delete: bool = False,
    audio_service: AudioService = Depends(AudioService),
    user: User = Depends(get_current_user),
) -> bool:
    await audio_service.delete_audio(
        audio_id=audio_id, full_delete=full_delete, user=user
    )
    return True
