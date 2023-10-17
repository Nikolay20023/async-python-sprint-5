import time
import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as redis
from sqlalchemy.future import select

from db.db import get_session
from core.config import mem_cache


logger = logging.getLogger(__name__)

router_base = APIRouter()


@router_base.get("/ping")
async def stattus(
    db: AsyncSession = Depends(get_session)
) -> dict:
    start: float  = time.time()
    await db.scalar(select(1))

    ping_db_duration = time.time() - start

    start_time_cache: float = time.time()
    mem_cache.ping()
    ping_cahce_durations: float = time.time() - start_time_cache

    return {
        "db": ping_db_duration,
        "cache": ping_cahce_durations
    }
    

