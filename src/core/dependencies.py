import jwt
from fastapi import Depends, HTTPException
from fastapi import Cookie

from src.crud import UserDAO
from src.models import User
from src.settings import settings


async def get_current_user(
    access_token: str = Cookie(None), db_user: UserDAO = Depends()
) -> User:
    """Получает аутентифицированного пользователя на основе JWT токена.

    Извлекает access token из куки, проверяет его валидность и возвращает
    соответствующего пользователя из базы данных.

    Args:
        access_token (str, optional): JWT токен из cookie. Defaults to None.
        db_user (UserDAO): DAO для работы с пользователями (внедряется через зависимость)

    Returns:
        User: Объект аутентифицированного пользователя

    Raises:
        HTTPException:
            401 - Если токен отсутствует или невалиден
            403 - Если пользователь деактивирован
    """
    if not access_token:
        raise HTTPException(status_code=401, detail="Токен отсутствует")

    token = access_token.replace("Bearer ", "")

    payload = jwt.decode(
        token, settings.ACCESS_SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    yandex_id: str = payload.get("sub")
    if yandex_id is None:
        raise HTTPException(status_code=401, detail="Неверный токен")

    user = await db_user.find_one(yandex_id=yandex_id)
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Пользователь деактивирован")
    return user


async def get_admin_user(
    user: User = Depends(get_current_user),
) -> User:
    if not user.is_supervisor:
        raise HTTPException(status_code=403, detail="У вас нет прав администратора")
    return user
