from datetime import datetime
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile
from uuid import UUID


import aiofiles
from fastapi import File, UploadFile
from fastapi.responses import FileResponse, StreamingResponse

from core.config import app_settings
from tools.base import join_user


async def write_file(path_dir: Path, file: UploadFile = File(), max_size: int = 1024**2):

    CHUNK_SIZE = 1024 * 100
    written_bytes = 0


    await file.seek(0)

    async with aiofiles.open(Path(path_dir, file.filename), "wb") as file_:
        while content := await file.read(CHUNK_SIZE):
            if written_bytes > max_size:
                raise Exception
            written_bytes += await file_.write(content)

    return written_bytes


async def get_file_by_path(user_id: UUID, user_name: str, path: str ="") -> FileResponse:
    full_path = get_path_to_subfolder(user_id, user_name, path)

    if not full_path.exists() or not full_path.is_file():
        raise Exception("File not found")

    return FileResponse(path=full_path)


def zip_directory(file_list: list[Path]) -> StreamingResponse:
    io = BytesIO()
    zip_name = f'{str(datetime.now())}.zip'
    with ZipFile(io, 'w') as zip_:
        for file_ in file_list:
            zip_.write(file_)

    return StreamingResponse(iter([io.getvalue()]),
                             media_type='application/x-zip-compressed',
                             headers={'Content-Disposition': f'attachment filename={zip_name}'})


def get_path_to_subfolder(user_id: int, user_name: str, path: str) -> Path:
    return Path.joinpath(Path.cwd(), app_settings.file_folder, join_user(user_id, user_name),
                         path)
