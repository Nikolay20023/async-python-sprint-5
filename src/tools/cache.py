import json 
import uuid
from datetime import datetime
from typing import Callable, Type

from fastapi_cache import caches
from fastapi_cache.backends.redis import CACHE_KEY, RedisCacheBackend
from pydantic import BaseModel


def redis_cahce():
    return caches.get(CACHE_KEY)


def serializer_data(value):
    if isinstance(value, datetime):
        return value.isoformat()
    elif isinstance(value, uuid.UUID):
        return str(value)
    return value


async def set_cahce(
    cache: RedisCacheBackend,
    data: dict,
    redis_key: str,
    expire: int = 30
):
    await cache.set(
        key=redis_key,
        value=json.dumps(data=data, default=serializer_data),
        expire=expire
    )
    

async def get_cahce(cache: RedisCacheBackend, redis_key: str) ->dict:
    data = await cache.get(redis_key)
    if data:
        data = json.loads(data)
    return data


async def get_cahce_or_data(
    redis_key: str,
    cache: RedisCacheBackend,
    db_func_obj: Callable,
    data_schema: Type[BaseModel],
    db_func_args: tuple = (),
    db_func_kwargs: dict = {},
    cache_expire: int = 30
):
    data = await get_cahce(cache, redis_key)
    if not data:
        data = await db_func_obj(*db_func_args, **db_func_kwargs)
        if data:
            data = data_schema.from_orm(data).dict()
            await set_cahce(
                cache=cache,
                data=data,
                redis_key=redis_key,
                expire=cache_expire
            )
        else:
            return None
    return data