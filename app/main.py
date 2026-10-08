import asyncio
import uvicorn
from .bot import bot, dp
from .config import settings
from .db import engine, Base

async def run():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    from .bot import dp
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(run())
