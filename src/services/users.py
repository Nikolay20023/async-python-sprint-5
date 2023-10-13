from typing import TypeVar, Generic, Type
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from sqlalchemy.future import select

from db.base import Base
from services.base import Repository
from schemas.users import UserCreate


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=UserCreate)


class UserDB(
    Repository, Generic[ModelType, CreateSchemaType]
):
    def __init__(self, model) -> None:
        self._model = model

    async def create(
        self,
        db: AsyncSession,
        *,
        obj_in: CreateSchemaType
    ):
        obj_data = jsonable_encoder(obj_in)
        db_obj = self._model(**obj_data)
        db.add(db_obj)
        await db.commit()
        return db_obj
    
    async def get(
        self,
        db: AsyncSession,
        *,
        username: str
    ):
        statement = select(self._model).where(self._model.username == username)
        user = await db.execute(statement)
        
        return user.scalar_one_or_none()

    async def get_multy(self, *args, **kwargs):
        return super().get_multy(*args, **kwargs)
    
    async def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)
    
    async def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)