from fastapi import Depends
from src.crud import UserDAO
from src.models import User
from src.schemas import UserInfo, UpdateUserInfo


class SupervisorService:
    def __init__(self, user_dao: UserDAO = Depends()):
        self._user_dao = user_dao


    async def process_user_info(self, user: User) -> UserInfo:
        return UserInfo(
            id=user.id,
            yandex_id=user.yandex_id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email
        )
    async def get_user(self, user_id: int) -> UserInfo:
        result = await self._user_dao.find_one(id=user_id)
        return await self.process_user_info(result)

    async def update_user(self, user_id: int, update_data: UpdateUserInfo) -> UserInfo:
        update_data = update_data.dict(exclude_none=True)

        if update_data:
            user_list = await self._user_dao.update(
                model_id=user_id, **update_data
            )
            user = user_list[0]
        else:
            user = await self._user_dao.find_one(id=user_id)

        return await self.process_user_info(user)
    
    async def delete_user(self, user_id: int, full_delete: bool = False) -> bool:
        if full_delete:
            await self._user_dao.delete(model_id=user_id)
        else:
            await self._user_dao.update(model_id=user_id, is_active=False)
        return True
