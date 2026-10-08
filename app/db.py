from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from .config import settings

url = settings.database_url
if url.startswith("postgresql://"):
    url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
elif url.startswith("postgres://"):
    url = url.replace("postgres://", "postgresql+asyncpg://", 1)

engine = create_async_engine(url, pool_pre_ping=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase):
    pass

async def get_session():
    async with SessionLocal() as session:
        yield session
