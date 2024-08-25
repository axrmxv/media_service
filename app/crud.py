from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import MediaFile
from app.schemas import MediaFileCreate


class MediaFileDAL:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_media_file(self,
                                media: MediaFileCreate,
                                uid: str) -> MediaFile:
        try:
            db_media = MediaFile(
                uid=uid,
                filename=media.filename,
                file_size=media.file_size,
                file_format=media.file_format,
                file_extension=media.file_extension
            )
            self.db.add(db_media)
            await self.db.commit()
            await self.db.refresh(db_media)
            return db_media
        except Exception as e:
            await self.db.rollback()
            raise e

    async def get_media_file(self, uid: str):
        # result = await self.db.execute(select(MediaFile)
        #                                .filter(MediaFile.uid == uid))
        # media_file = result.scalars().first()
        # return media_file
        query = select(MediaFile).where(MediaFile.uid == uid)
        result = await self.db.execute(query)
        return result.scalars().first()
