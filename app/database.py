# from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from env_settings import DATABASE_URL

# from app.models import Base

from typing import AsyncGenerator


# engine = create_engine(DATABASE_URL)
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    )
# Base.metadata.create_all(bind=engine)

async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
    )


async def get_session() -> AsyncGenerator:
    async with async_session() as session:
        yield session
