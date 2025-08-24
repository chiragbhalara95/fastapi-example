from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "sqlite+aiosqlite:///./app.db"  # change to postgres later

# Async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Async session
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Base for models
class Base(DeclarativeBase):
    pass

# Dependency
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
