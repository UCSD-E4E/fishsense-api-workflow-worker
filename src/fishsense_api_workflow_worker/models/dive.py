from datetime import datetime

from sqlmodel import Field, SQLModel

from fishsense_api_workflow_worker.models.priority import Priority


class Dive(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    path: str = Field(max_length=255, unique=True, index=True)
    dive_datetime: datetime = Field(default=None)
    priority: Priority = Field(default=Priority.LOW, index=True)

    camera_id: int | None = Field(default=None, foreign_key="camera.id")
