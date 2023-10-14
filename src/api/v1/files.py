from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, status, File    


router_files = APIRouter()


@router_files.post("/files")
async def create_files(file: UploadFile = File()):
    return {
        "file": file
    }