from functools import wraps
from fastapi import HTTPException
from sqlalchemy.exc import DataError as SQLAlchemyDataError, DBAPIError
from asyncpg.exceptions import DataError as AsyncPGDataError


def handle_db_errors(func):

    @wraps(func)
    async def wrapper(*args, **kwargs):
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
