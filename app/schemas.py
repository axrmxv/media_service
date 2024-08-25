from pydantic import BaseModel


class MediaFileBase(BaseModel):
    filename: str
    file_size: int
    file_format: str
    file_extension: str


class MediaFileCreate(MediaFileBase):
    pass


class MediaFile(MediaFileBase):
    id: int
    uid: str

    class Config:
        orm_mode = True
