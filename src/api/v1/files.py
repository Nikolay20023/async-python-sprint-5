from typing import Union, List

from fastapi import APIRouter, Depends, UploadFile, status, File
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession    

from .users import get_current_user
from db.db import get_session
from core.exceptions import (FileNotCreatedError, FileNotFoundHttpError,
                             FileNotFoundInStorageError, InternalServerErrorHttpError,
                             UpladedFileExceedError)
from models.models import User
from services.entity import files_crud
from schemas.files import FileInDB, UploadResponse
# from services.files import

router_files = APIRouter()


@router_files.post("/files")
async def create_files(file: UploadFile = File()):
    return {
        "file": file
    }


@router_files.get("/list")
async def get_files_list(
    db: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user)
):
    
    files: List = await files_crud.get_multy(db=db, user=user)
    return [FileInDB(**file.__dict__) for file in files]
    

@router_files.post('/upload',
             status_code=status.HTTP_201_CREATED,
             description='Upload user file.',
             response_model=UploadResponse,)
async def upload_file(
        subdir: str = '',
        file: UploadFile = File(),
        db: AsyncSession = Depends(get_session),
        user: User = Depends(get_current_user),
) -> UploadResponse:
    try:
        file_upload: dict = await files_crud.create(db=db, file=file, user=user, path=subdir)
    except UpladedFileExceedError:
        raise FileNotFoundHttpError(detail='Превышен размер файла')
    except FileNotCreatedError:
        raise InternalServerErrorHttpError(detail='Не удалось создать файл')
    except SQLAlchemyError:
        raise InternalServerErrorHttpError(detail='Не удалось добавить запись о файле')

    return UploadResponse(**file_upload)
# @router_files.get("/upload", status_code=status.HTTP_201_CREATED)
# async def upload_file(
#     subdir: str = "",
#     file: UploadFile = File(),
#     db: AsyncSession = Depends(get_session),
#     user: User = Depends(get_current_user)
# ):
#     try:
#         file_upload: dict = await