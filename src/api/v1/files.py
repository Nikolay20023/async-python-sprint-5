from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, status, File
from sqlalchemy.ext.asyncio import AsyncSession    

from users import get_current_user

router_files = APIRouter()


@router_files.post("/files")
async def create_files(file: UploadFile = File()):
    return {
        "file": file
    }


@router_files.get("/lits")
async def get_list(
    *,
    db: AsyncSession,
    current_user = Depends(get_current_user),
    cache
):
    redis_key = f"files_list_for_{str(current_user.id)}"
    data = await get_cache(cache, redis_key)
    if not data