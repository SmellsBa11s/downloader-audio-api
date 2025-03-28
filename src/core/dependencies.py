import jwt
from fastapi import Depends, HTTPException
from fastapi import Cookie

from src.crud import UserDAO
from src.models import User
from src.settings import settings


async def get_current_user(
    access_token: str = Cookie(None), db_user: UserDAO = Depends()
) -> User:
    """Get the authenticated user based on JWT token.

    Extracts the access token from cookies, validates it, and returns
    the corresponding user from the database.

    Args:
        access_token (str, optional): JWT token from cookie. Defaults to None.
        db_user (UserDAO): DAO for user operations (injected via dependency)

    Returns:
        User: Authenticated user object

    Raises:
        HTTPException:
            401 - If token is missing or invalid
            403 - If user is deactivated
    """
    if not access_token:
        raise HTTPException(status_code=401, detail="Token is missing")

    token = access_token.replace("Bearer ", "")

    payload = jwt.decode(
        token, settings.ACCESS_SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    yandex_id: str = payload.get("sub")
    if yandex_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await db_user.find_one(yandex_id=yandex_id)
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User is deactivated")
    return user


async def get_admin_user(
    user: User = Depends(get_current_user),
) -> User:
    """Get the authenticated admin user.

    This dependency ensures that the authenticated user has admin privileges.
    It depends on get_current_user to first authenticate the user.

    Args:
        user (User): The authenticated user (injected via get_current_user dependency)

    Returns:
        User: The authenticated admin user

    Raises:
        HTTPException:
            403 - If the user is not an admin
    """
    if not user.is_supervisor:
        raise HTTPException(
            status_code=403, detail="You don't have administrator privileges"
        )
    return user
