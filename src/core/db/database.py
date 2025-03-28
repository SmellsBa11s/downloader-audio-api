from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from typing import AsyncGenerator

from src.settings import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """Get an async database session.

    This function creates and yields an async database session.
    The session is automatically closed after use.

    Yields:
        AsyncSession: An async database session

    Note:
        This function should be used as a FastAPI dependency.
        The session is automatically closed when the request is complete.
    """
    db = async_session()
    try:
        yield db
    finally:
        await db.close()
