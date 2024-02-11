from datetime import datetime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Date


class Base(DeclarativeBase):
    pass


class DoogleDoor(Base):
    __tablename__ = "usage"

    id: Mapped[int] = mapped_column(primary_key=True)
    published: Mapped[int]
    published_tz: Mapped[datetime]
