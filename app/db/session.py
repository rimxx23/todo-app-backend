from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from app.core.config import get_settings


settings = get_settings()
engine = create_async_engine(settings.DATABASE_URL)
Sessionlocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_db():
    db = Sessionlocal()

    try:
        yield db
    finally:
        await db.close()
