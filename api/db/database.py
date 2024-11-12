from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from api.db.base_model import Model
from config import settings

engine = create_async_engine(settings.get_async_uri())
new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_db():
    db = new_session()
    try:
        yield db
    finally:
        await db.close()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
