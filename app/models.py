from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()


class MediaFile(Base):
    """Модель для представления медиафайлов в базе данных."""

    __tablename__ = "media_files"

    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String, unique=True, index=True)
    filename = Column(String, index=True)
    file_size = Column(Integer)
    file_format = Column(String)
    file_extension = Column(String)
