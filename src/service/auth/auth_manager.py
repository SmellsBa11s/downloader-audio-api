from fastapi import Depends, Response
from src.crud.user import UserDAO
from src.service.auth.yandex_auth import YandexAuthService
from src.service.auth.token_service import TokenService
from src.service.auth.payload import PayloadService


class AuthManager(YandexAuthService, TokenService, PayloadService):
    def __init__(self, user_dao: UserDAO = Depends()):
        """Инициализация AuthManager с необходимыми зависимостями."""
        YandexAuthService.__init__(self, user_dao)
        TokenService.__init__(self, self)
        PayloadService.__init__(self)
        self._user_dao = user_dao

    async def authenticate_and_set_tokens(self, code: str, response: Response) -> dict:
        """Комбинированный метод для аутентификации через Яндекс и установки токенов."""
        user = await self.authenticate_yandex(code)
        return self.generate_and_set_tokens(response, user)
