from typing import List
from fastapi import APIRouter, Depends
from src.core.dependencies import get_admin_user
from src.models import User
from src.schemas import UserInfo, UpdateUserInfo, AudioFullInfo
from src.service import SupervisorService


router = APIRouter()


@router.get("/{user_id}")
async def get_user_info(
    user_id: int,
    supervisor_service: SupervisorService = Depends(),
    user: User = Depends(get_admin_user),
) -> UserInfo:
    return await supervisor_service.get_user(user_id)


@router.get("/{user_id}/audio")
async def get_user_audio(
    user_id: int,
    supervisor_service: SupervisorService = Depends(),
    user: User = Depends(get_admin_user),
) -> List[AudioFullInfo]:
    return await supervisor_service.get_user_audio(user_id)


@router.put("/{user_id}")
async def update_user(
    user_id: int,
    user_info: UpdateUserInfo,
    supervisor_service: SupervisorService = Depends(),
    user: User = Depends(get_admin_user),
) -> UserInfo:
    return await supervisor_service.update_user(user_id=user_id, update_data=user_info)


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    full_delete: bool = False,
    supervisor_service: SupervisorService = Depends(),
    user: User = Depends(get_admin_user),
) -> bool | UserInfo:
    return await supervisor_service.delete_user(
        user_id=user_id, full_delete=full_delete
    )


@router.post("/activate-user/")
async def activate_user(
    user_id: int,
    supervisor_service: SupervisorService = Depends(SupervisorService),
    user: User = Depends(get_admin_user),
) -> bool:
    return await supervisor_service.activate_user(user_id=user_id)
