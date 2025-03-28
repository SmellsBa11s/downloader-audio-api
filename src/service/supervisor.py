from fastapi import Depends
from src.crud import UserDAO, AudioDAO
from src.models import User
from src.schemas import UserInfo, UpdateUserInfo, AudioFullInfo


class SupervisorService:
    def __init__(self, user_dao: UserDAO = Depends(), audio_dao: AudioDAO = Depends()):
        self._user_dao = user_dao
        self._audio_dao = audio_dao

    async def process_user_info(self, user: User) -> UserInfo:
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
        result = await self._user_dao.find_one(id=user_id)
        return await self.process_user_info(result)

    async def update_user(self, user_id: int, update_data: UpdateUserInfo) -> UserInfo:
        update_data = update_data.dict(exclude_none=True)
        user = await self._user_dao.find_one(id=user_id, is_active=True)

        if update_data:
            user_list = await self._user_dao.update(model_id=user_id, **update_data)
            user = user_list[0]

        return await self.process_user_info(user)

    async def delete_user(self, user_id: int, full_delete: bool = False) -> bool:
        await self._user_dao.find_one(id=user_id, is_active=True)
        if full_delete:
            await self._user_dao.delete(model_id=user_id)
        else:
            await self._user_dao.update(model_id=user_id, is_active=False)
        return True

    async def activate_user(self, user_id: int) -> bool:
        await self._user_dao.update(model_id=user_id, is_active=True)
        return True

    async def get_user_audio(self, user_id: int) -> list[AudioFullInfo]:
        """Получает список аудио файлов пользователя."""
        await self._user_dao.find_one(id=user_id, is_active=True)
        audio_files = await self._audio_dao.find_all(user_id=user_id, is_deleted=False)
        return [
            AudioFullInfo(
                audio_id=audio.id,
                filename=audio.filename,
                user_id=audio.user_id,
                path=audio.path,
                size=audio.size,
                created_at=audio.created_at,
            )
            for audio in audio_files
        ]
