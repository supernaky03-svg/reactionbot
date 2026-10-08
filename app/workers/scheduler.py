import asyncio
from datetime import datetime
from sqlalchemy import select
from ..db import SessionLocal
from ..models import ReactionTask

async def scheduler_loop():
    while True:
        async with SessionLocal() as s:
            q = await s.execute(select(ReactionTask).where(
                ReactionTask.status == "scheduled", ReactionTask.scheduled_at <= datetime.utcnow()
            ).limit(100))
            tasks = q.scalars().all()
            for task in tasks:
                task.status = "processing"
            await s.commit()
        await asyncio.sleep(2)
