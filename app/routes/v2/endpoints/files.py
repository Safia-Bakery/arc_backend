from fastapi import APIRouter, UploadFile
from fastapi import Depends, File
from sqlalchemy.orm import Session

from app.routes.depth import get_db, get_current_user
from app.schemas.users import GetUserFullData
from app.utils.utils import generate_random_string

file_router = APIRouter()


@file_router.post("/file/upload",)
async def read_files(
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: GetUserFullData = Depends(get_current_user),
):
    file_paths = []
    for file in files:
        file_path = f"files/{generate_random_string(10)}{file.filename}"
        with open(file_path, "wb") as buffer:
            while True:
                chunk = await file.read(1024)
                if not chunk:
                    break
                buffer.write(chunk)
        file_paths.append(file_path)
    return {"files": file_paths}

