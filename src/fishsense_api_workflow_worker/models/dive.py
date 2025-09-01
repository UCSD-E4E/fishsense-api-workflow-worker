from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Dive(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    path: str = Field(max_length=255, unique=True, index=True)
    dive_datetime: datetime = Field(default=None)

    camera_id: int | None = Field(default=None, foreign_key="camera.id")
