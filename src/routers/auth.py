from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Cookie, Response
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import RedirectResponse

from src.crud import UserDAO
from src.service import AuthManager
from src.schemas import AuthResponse, RedirectResponse
from src.settings import settings

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/login/yandex")
async def yandex_login():
    """Redirect to Yandex OAuth login page.

    Returns:
        RedirectResponse: Response that redirects to Yandex OAuth login page
    """
    return RedirectResponse(redirect_url=settings.YANDEX_REDIRECT_URL)


@router.get("/yandex/callback")
async def yandex_callback(
    code: str, response: Response, auth_manager: AuthManager = Depends()
):
    """Handle Yandex OAuth callback.

    This endpoint processes the OAuth callback from Yandex, authenticates the user,
    and sets authentication tokens in cookies.

    Args:
        code (str): Authorization code from Yandex OAuth
        response (Response): FastAPI response object
        auth_manager (AuthManager): Authentication manager service

    Returns:
        AuthResponse: Authentication tokens

    Raises:
        HTTPException: 400 if authentication fails
    """
    tokens = await auth_manager.authenticate_and_set_tokens(code=code, response=response)
    return AuthResponse(**tokens)


@router.post("/refresh", summary="Refresh access token")
async def refresh_token_api(
    response: Response,
    refresh_token: Optional[str] = Cookie(default=None),
    auth_manager: AuthManager = Depends(),
    db_user: UserDAO = Depends(),
) -> AuthResponse:
    """Refresh the access token using a refresh token.

    This endpoint allows users to obtain a new access token using their refresh token.
    The refresh token is read from cookies, and new tokens are set in the response.

    Args:
        response (Response): FastAPI response object
        refresh_token (Optional[str]): Refresh token from cookies
        auth_manager (AuthManager): Authentication manager service
        db_user (UserDAO): Data access object for user operations

    Returns:
        AuthResponse: New authentication tokens

    Raises:
        HTTPException:
            401 - If refresh token is missing or invalid
            404 - If user not found
    """
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token is missing")

    try:
        payload = auth_manager.get_token_payload(token=refresh_token, is_refresh=True)
        yandex_id = payload.get("sub")
        if not yandex_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        user = await db_user.find_one(yandex_id=yandex_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        tokens = auth_manager.generate_and_set_tokens(response=response, user=user)
        return AuthResponse(**tokens)

    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
