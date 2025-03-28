from fastapi import Depends
from src.crud import UserDAO, AudioDAO
from src.models import User
from src.schemas import UserInfo, UpdateUserInfo, AudioFullInfo


class SupervisorService:
    """Service for managing users and their audio files.

    This service provides functionality for user management and audio file operations
    with administrative privileges.

    Attributes:
        _user_dao (UserDAO): Data access object for user operations
        _audio_dao (AudioDAO): Data access object for audio file operations
    """

    def __init__(self, user_dao: UserDAO = Depends(), audio_dao: AudioDAO = Depends()):
        """Initialize the supervisor service.

        Args:
            user_dao (UserDAO): Data access object for user operations
            audio_dao (AudioDAO): Data access object for audio file operations
        """
        self._user_dao = user_dao
        self._audio_dao = audio_dao

    async def process_user_info(self, user: User) -> UserInfo:
        """Convert User model to UserInfo schema.

        Args:
            user (User): SQLAlchemy User model instance

        Returns:
            UserInfo: Pydantic model with user information
        """
        return UserInfo(
            id=user.id,
            yandex_id=user.yandex_id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            is_active=user.is_active,
            is_supervisor=user.is_supervisor,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    async def get_user(self, user_id: int) -> UserInfo:
        """Get user information by ID.

        Args:
            user_id (int): ID of the user to retrieve

        Returns:
            UserInfo: User information

        Raises:
            HTTPException: 404 if user not found
        """
        result = await self._user_dao.find_one(id=user_id)
        return await self.process_user_info(result)

    async def update_user(self, user_id: int, update_data: UpdateUserInfo) -> UserInfo:
        """Update user information.

        Args:
            user_id (int): ID of the user to update
            update_data (UpdateUserInfo): New user information

        Returns:
            UserInfo: Updated user information

        Raises:
            HTTPException: 404 if user not found or inactive
        """
        update_data = update_data.dict(exclude_none=True)
        user = await self._user_dao.find_one(id=user_id, is_active=True)

        if update_data:
            user_list = await self._user_dao.update(model_id=user_id, **update_data)
            user = user_list[0]

        return await self.process_user_info(user)

    async def delete_user(self, user_id: int, full_delete: bool = False) -> bool:
        """Delete or deactivate a user.

        Args:
            user_id (int): ID of the user to delete
            full_delete (bool, optional): If True, permanently delete the user.
                If False, only deactivate the user. Defaults to False.

        Returns:
            bool: True if operation was successful

        Raises:
            HTTPException: 404 if user not found or inactive
        """
        if full_delete:
            await self._user_dao.delete(model_id=user_id)
        else:
            await self._user_dao.find_one(id=user_id, is_active=True)
            await self._user_dao.update(model_id=user_id, is_active=False)
        return True

    async def activate_user(self, user_id: int) -> bool:
        """Activate a previously deactivated user.

        Args:
            user_id (int): ID of the user to activate

        Returns:
            bool: True if activation was successful

        Raises:
            HTTPException: 404 if user not found
        """
        await self._user_dao.update(model_id=user_id, is_active=True)
        return True

    async def get_user_audio(self, user_id: int, include_deleted: bool = False) -> list[AudioFullInfo]:
        """Get list of user's audio files.

        Args:
            user_id (int): ID of the user whose audio files to retrieve

        Returns:
            list[AudioFullInfo]: List of user's audio files

        Raises:
            HTTPException: 404 if user not found or inactive
        """
        await self._user_dao.find_one(id=user_id, is_active=True)
        if include_deleted:
            audio_files = await self._audio_dao.find_all(user_id=user_id)
        else:
            audio_files = await self._audio_dao.find_all(user_id=user_id, is_deleted=False)
        return [
            AudioFullInfo(
                audio_id=audio.id,
                filename=audio.filename,
                is_deleted=audio.is_deleted,
                user_id=audio.user_id,
                path=audio.path,
                size=audio.size,
                created_at=audio.created_at,
            )
            for audio in audio_files
        ]
