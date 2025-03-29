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
    """Get user information.

    This endpoint allows administrators to retrieve information about any user.

    Args:
        user_id (int): ID of the user to retrieve
        supervisor_service (SupervisorService): Service for user management
        user (User): Current authenticated admin user

    Returns:
        UserInfo: User information

    Raises:
        HTTPException: 404 if user not found
    """
    return await supervisor_service.get_user(user_id=user_id)


@router.get("/{user_id}/audio")
async def get_user_audio(
    user_id: int,
    include_deleted: bool = False,
    supervisor_service: SupervisorService = Depends(),
    user: User = Depends(get_admin_user),
) -> List[AudioFullInfo]:
    """Get user's audio files.

    This endpoint allows administrators to retrieve all audio files
    associated with a specific user.

    Args:
        user_id (int): ID of the user whose audio files to retrieve
        supervisor_service (SupervisorService): Service for user management
        user (User): Current authenticated admin user

    Returns:
        List[AudioFullInfo]: List of user's audio files

    Raises:
        HTTPException: 404 if user not found
    """
    return await supervisor_service.get_user_audio(
        user_id=user_id, include_deleted=include_deleted
    )


@router.put("/{user_id}")
async def update_user(
    user_id: int,
    user_info: UpdateUserInfo,
    supervisor_service: SupervisorService = Depends(),
    user: User = Depends(get_admin_user),
) -> UserInfo:
    """Update user information.

    This endpoint allows administrators to update information about any user.

    Args:
        user_id (int): ID of the user to update
        user_info (UpdateUserInfo): New user information
        supervisor_service (SupervisorService): Service for user management
        user (User): Current authenticated admin user

    Returns:
        UserInfo: Updated user information

    Raises:
        HTTPException: 404 if user not found
    """
    return await supervisor_service.update_user(user_id=user_id, update_data=user_info)


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    full_delete: bool = False,
    supervisor_service: SupervisorService = Depends(),
    user: User = Depends(get_admin_user),
) -> bool | UserInfo:
    """Delete or deactivate a user.

    This endpoint allows administrators to delete or deactivate any user.
    When full_delete is False, the user is only deactivated.

    Args:
        user_id (int): ID of the user to delete
        full_delete (bool, optional): If True, permanently delete the user.
            If False, only deactivate the user. Defaults to False.
        supervisor_service (SupervisorService): Service for user management
        user (User): Current authenticated admin user

    Returns:
        bool | UserInfo: True if deletion was successful, or UserInfo if user was deactivated

    Raises:
        HTTPException: 404 if user not found
    """
    return await supervisor_service.delete_user(
        user_id=user_id, full_delete=full_delete
    )


@router.post("/activate-user/")
async def activate_user(
    user_id: int,
    supervisor_service: SupervisorService = Depends(SupervisorService),
    user: User = Depends(get_admin_user),
) -> bool:
    """Activate a previously deactivated user.

    This endpoint allows administrators to reactivate a deactivated user account.

    Args:
        user_id (int): ID of the user to activate
        supervisor_service (SupervisorService): Service for user management
        user (User): Current authenticated admin user

    Returns:
        bool: True if activation was successful

    Raises:
        HTTPException: 404 if user not found
    """
    return await supervisor_service.activate_user(user_id=user_id)
