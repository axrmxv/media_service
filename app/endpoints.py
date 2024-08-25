import os
import uuid
import shutil

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from fastapi.responses import FileResponse

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.schemas import MediaFileCreate, MediaFile
from app.crud import MediaFileDAL
from app.cloud_storage import upload_to_cloud


upload_media = APIRouter()
get_media = APIRouter()


@get_media.get("/{uid}")
async def get_file(uid: str, db: AsyncSession = Depends(get_session)):
    gfile = MediaFileDAL(db)
    db_file = await gfile.get_media_file(uid)

    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")

    file_path = f"file_storage/{uid}_{db_file.filename}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found on disk")

    return FileResponse(path=file_path,
                        filename=db_file.filename,
                        media_type=db_file.file_format)


@upload_media.post("/", response_model=MediaFile)
async def upload_file(file: UploadFile = File(...),
                      db: AsyncSession = Depends(get_session)):
    try:
        uid = str(uuid.uuid4())

        storage_directory = "file_storage"
        if not os.path.exists(storage_directory):
            os.makedirs(storage_directory)

        # Полный путь к файлу
        file_location = os.path.join(storage_directory,
                                     f"{uid}_{file.filename}")
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)

        file_size = os.path.getsize(file_location)
        file_extension = os.path.splitext(file.filename)[1].replace(".", "")
        file_format = file.content_type

        media_file = MediaFileCreate(
            filename=file.filename,
            file_size=file_size,
            file_format=file_format,
            file_extension=file_extension,
        )
        new_file = MediaFileDAL(db)
        db_file = await new_file.create_media_file(media_file, uid)

        await upload_to_cloud(file_location, uid)

        return db_file
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
