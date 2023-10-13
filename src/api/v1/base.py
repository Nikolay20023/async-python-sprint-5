import time
import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.future import select

from db.db import get_session


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/ping")
async def stattus(
    db: AsyncSession = Depends(get_session)
) -> dict:
    start: float  = time.time()
    await db.scalar(select(1))

    ping_db_duration = time.time() - start

