from typing import Optional

from sqlmodel import Field, SQLModel


class Camera(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    serial_number: str = Field(unique=True, index=True)
    name: str = Field(unique=True, index=True)
