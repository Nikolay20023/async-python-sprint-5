# from src.core.config import app_settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


# app_settings.database_dsn,
engine = create_async_engine(
    "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres",
    echo=True,
    future=True
)

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
