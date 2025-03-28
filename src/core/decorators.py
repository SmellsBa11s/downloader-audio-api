from functools import wraps
from typing import Any, Callable, TypeVar, ParamSpec
from fastapi import HTTPException
from sqlalchemy.exc import DataError as SQLAlchemyDataError, DBAPIError
from asyncpg.exceptions import DataError as AsyncPGDataError

P = ParamSpec("P")
T = TypeVar("T")


def handle_db_errors(func: Callable[P, T]) -> Callable[P, T]:
    """Decorator for handling database-related errors in async functions.

    This decorator wraps async functions to handle common database errors and provides
    appropriate HTTP responses. It handles SQLAlchemy and AsyncPG specific errors,
    performs session rollback if available, and converts database errors to HTTP exceptions.

    Args:
        func (Callable[P, T]): The async function to be decorated.

    Returns:
        Callable[P, T]: Wrapped function with error handling.

    Raises:
        HTTPException:
            400 - If the value is out of int32 range
            409 - For other database-related errors
    """

    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        try:
            return await func(*args, **kwargs)
        except (SQLAlchemyDataError, AsyncPGDataError, DBAPIError) as e:
            if hasattr(args[0], "session"):
                await args[0].session.rollback()
            if "value out of int32 range" in str(e):
                raise HTTPException(
                    status_code=400,
                    detail="Некорректные данные: значение выходит за пределы допустимого диапазона",
                )
            raise HTTPException(status_code=409, detail=f"Database error: {str(e)}")
        except Exception as e:
            if hasattr(args[0], "session"):
                await args[0].session.rollback()
            raise HTTPException(status_code=409, detail=f"Database error: {str(e)}")

    return wrapper
