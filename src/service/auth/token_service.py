from fastapi import Response
from src.settings import settings
from src.service.auth.payload import PayloadService
from src.models.user import User

class TokenService:
    def __init__(self, payload_service: PayloadService):
        self.payload_service = payload_service

    def set_auth_cookies(self, response: Response, tokens: dict) -> None:
        """Устанавливает куки для аутентификации."""
        response.set_cookie(
            key="access_token",
            value=f"Bearer {tokens['access_token']}",
            httponly=True,
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            secure=True,
            samesite="lax",
        )

        response.set_cookie(
            key="refresh_token",
            value=f"Bearer {tokens['refresh_token']}",
            httponly=True,
            max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
            secure=True,
            samesite="lax",
        )

    def generate_and_set_tokens(self, response: Response, user: User) -> dict:
        """Генерирует токены и устанавливает их в куки."""
        tokens = self.payload_service.generate_tokens(user)
        self.set_auth_cookies(response, tokens)
        return tokens 