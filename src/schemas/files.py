from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class ORM(BaseModel):
    class Config:
        orm_mode = True


class FileBase(ORM):
    name: str


class FileCreater(FileBase):
    pass


class FileUpload(ORM):
    path: str


class FileInDBase(FileBase):
    id: UUID
    created_at: datetime
    path: Optional[str]
    size: float
    is_downloadable: bool


class File(FileInDBase):
    pass


class FileInDB(FileInDBase):
    pass


class UploadResponse(ORM):
    status: Optional[str] = None
    size: Optional[str] = None
