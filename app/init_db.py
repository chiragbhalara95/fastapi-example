import asyncio
from app.db import engine, Base
from app.models.item import Item

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_models())
