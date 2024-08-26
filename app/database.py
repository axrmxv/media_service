from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from env_settings import DATABASE_URL

from typing import AsyncGenerator


# Создаем асинхронный движок для работы с базой данных
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    )

# Создаем фабрику асинхронных сессий
async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
    )


# Генератор для предоставления сессии базы данных в FastAPI через зависимость
async def get_session() -> AsyncGenerator:
    async with async_session() as session:
        yield session
