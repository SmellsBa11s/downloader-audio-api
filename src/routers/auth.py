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
    """Перенаправление на страницу авторизации Яндекс."""
    return RedirectResponse(redirect_url=settings.YANDEX_REDIRECT_URL)


@router.get("/yandex/callback")
async def yandex_callback(
    code: str, response: Response, auth_manager: AuthManager = Depends()
):
    tokens = await auth_manager.authenticate_and_set_tokens(code, response)
    return AuthResponse(**tokens)


@router.post("/refresh", summary="Refresh access token")
async def refresh_token_api(
    response: Response,
    refresh_token: Optional[str] = Cookie(default=None),
    auth_manager: AuthManager = Depends(),
    db_user: UserDAO = Depends(),
) -> AuthResponse:
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token is missing")

    try:
        payload = auth_manager.get_token_payload(refresh_token, is_refresh=True)
        yandex_id = payload.get("sub")
        if not yandex_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        user = await db_user.find_one(yandex_id=yandex_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        tokens = auth_manager.generate_and_set_tokens(response, user)
        return AuthResponse(**tokens)

    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
