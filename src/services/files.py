from typing import TypeVar, Generic
from typing import Union
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from fastapi import UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.future import select
from pydantic import BaseModel
from pathlib import Path

from db.base import Base
from services.base import Repository
from core.logger import logger
from schemas.files import FileCreater
from models.models import User
from core.exceptions import (FileNotCreatedError, FileNotFoundInStorageError,
                             InputTypeNotSupportedError)
from tools.files import get_file_by_path, get_path_to_subfolder, write_file, zip_directory


ModelType = TypeVar("ModelType", bound=Base) 
CreateSchemaType = TypeVar("CreateSchemaType", bound=FileCreater)


class FileDB(
    Repository, Generic[ModelType, CreateSchemaType]
):
    def __init__(self, model) -> None:
        self._model = model

    async def create(
        self,
        *,
        db: AsyncSession,
        user: User,
        path: str ="",
        file: UploadFile = File()
    ):
        directory_path_ = get_path_to_subfolder(user.id, user.username, path)
        # if not directory_path_.exists():
        #     directory_path_.mkdir(parents=True, exist_ok=True)
        
        written_bytes = await write_file(path_dir=directory_path_, file=file)
        logger.info(f"Write bytes: {written_bytes}")
        if Path.exists(Path.joinpath(directory_path_, file.filename)):
            await self._create_db_record(
                db=db,
                user=user,
                path=path,
                filename=file.filename,
                size=written_bytes,
            )
            size_ = "{:.3f}".format(written_bytes / 1024)    # noqa Q000
            return {
                'status': f'Successfully uploaded {file.filename}',
                'size': f'{size_} kb',
            }
        raise FileNotCreatedError()

    async def get_multy(
        self,
        *,
        db: AsyncSession, 
        user: User
    ):
        statement = select(self._model).where(self._model.user_id == user.id)
        list_files = await db.scalar(statement=statement)

        return list_files.all()

    async def _create_db_record(
        self,
        size: int,
        db: AsyncSession,
        user: User,
        path: str,
        filename: str
    ) -> ModelType:
        file_record = self._model(
            name=filename,
            path=path,
            size=size,
            user_id=user.id
        )

        db.add(file_record)
        db.commit()

        return file_record
    
    async def _get_path_by_id(self, db: AsyncSession, user: ModelType, id_: int) -> Path:
        statement = select(self._model).where(self._model.id == id_)
        file_record_ = await db.scalar(statement=statement)
        return Path.joinpath(get_path_to_subfolder(user.id, user.username, file_record_.path),
                             file_record_.name)

    async def _get_file_by_id(self, db: AsyncSession, user: User, id_: int) -> FileResponse:
        file_path_ = await self._get_path_by_id(db=db, id_=id_, user=user)
        if not file_path_.exists() or not file_path_.is_file():
            raise FileNotFoundInStorageError()

        return FileResponse(path=file_path_)
    
    async def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)
    
    async def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)
    
    async def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)