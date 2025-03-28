from fastapi import Depends, HTTPException
import httpx
from passlib.context import CryptContext
from src.crud.user import UserDAO
from src.models import User
from src.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class YandexAuthService:
    def __init__(self, user_dao: UserDAO = Depends()):
        """Initializes DAO for working with users.

        Args:
            user_dao (UserDAO): DAO for working with users
        """
        self._user_dao = user_dao

    @staticmethod
    async def get_yandex_user(code: str) -> dict:
        """Получает данные пользователя от Яндекс OAuth."""
        token_url = "https://oauth.yandex.ru/token"
        token_data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": settings.YANDEX_CLIENT_ID,
            "client_secret": settings.YANDEX_CLIENT_SECRET,
        }

        async with httpx.AsyncClient() as client:
            token_response = await client.post(token_url, data=token_data)
            if token_response.status_code != 200:
                raise HTTPException(status_code=400, detail="Invalid code")

            access_token = token_response.json()["access_token"]

            user_response = await client.get(
                "https://login.yandex.ru/info",
                params={"format": "json"},
                headers={"Authorization": f"OAuth {access_token}"},
            )
            if user_response.status_code != 200:
                raise HTTPException(status_code=400, detail="Failed to get user info")

            user_data = user_response.json()
            return user_data

    async def authenticate_yandex(self, code: str) -> User:
        """Авторизация/регистрация через Яндекс."""
        yandex_data = await self.get_yandex_user(code)

        user = await self._user_dao.find_one_or_none(yandex_id=yandex_data["id"])
        if user:
            return user

        user_data = {
            "yandex_id": yandex_data["id"],
            "email": yandex_data.get("default_email"),
            "first_name": yandex_data.get("first_name"),
            "last_name": yandex_data.get("last_name"),
        }
        created_user = await self._user_dao.add(user_data)
        return created_user
