from fastapi import Depends, Response
from src.crud.user import UserDAO
from src.service.auth.yandex_auth import YandexAuthService
from src.service.auth.token_service import TokenService
from src.service.auth.payload import PayloadService


class AuthManager(YandexAuthService, TokenService, PayloadService):
    """Service for managing authentication operations.

    This class combines functionality from YandexAuthService, TokenService, and PayloadService
    to provide a complete authentication flow.

    Attributes:
        _user_dao (UserDAO): Data access object for user operations
    """

    def __init__(self, user_dao: UserDAO = Depends()):
        """Initialize AuthManager with required dependencies.

        Args:
            user_dao (UserDAO): Data access object for user operations
        """
        YandexAuthService.__init__(self, user_dao)
        TokenService.__init__(self, self)
        PayloadService.__init__(self)
        self._user_dao = user_dao

    async def authenticate_and_set_tokens(self, code: str, response: Response) -> dict:
        """Authenticate user through Yandex and set authentication tokens.

        This method combines Yandex authentication and token generation/setting
        into a single operation.

        Args:
            code (str): Authorization code from Yandex OAuth
            response (Response): FastAPI response object for setting cookies

        Returns:
            dict: Generated authentication tokens

        Raises:
            HTTPException: 400 if authentication fails
        """
        user = await self.authenticate_yandex(code)
        return self.generate_and_set_tokens(response, user)
