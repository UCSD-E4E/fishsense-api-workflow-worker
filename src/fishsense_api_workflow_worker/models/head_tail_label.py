"""This module defines the HeadTailLabel model, which represents a head-tail label"""

import json
import logging
from datetime import datetime
from typing import Any, Dict

from sqlmodel import JSON, Column, DateTime, Field, SQLModel


class HeadTailLabel(SQLModel, table=True):
    """Model representing a head-tail label."""

    id: int | None = Field(default=None, primary_key=True)
    label_studio_task_id: int | None = Field(default=None, unique=True, index=True)
    head_x: int | None = Field(default=None)
    head_y: int | None = Field(default=None)
    tail_x: int | None = Field(default=None)
    tail_y: int | None = Field(default=None)
    updated_at: datetime | None = Field(sa_type=DateTime(timezone=True), default=None)
    json: Dict[str, Any] | None = Field(default=None, sa_column=Column(JSON))

    image_id: int | None = Field(default=None, foreign_key="image.id")
    user_id: int | None = Field(default=None, foreign_key="user.id")

    @classmethod
    def from_task(cls, task: Any) -> "HeadTailLabel":
        """Create a HeadTailLabel instance from a Label Studio task."""

        log = logging.getLogger("HeadTailLabel")
        log.debug("Initializing HeadTailLabel with task ID: %s", task.id)

        return cls(
            label_studio_task_id=task.id,
            head_x=cls.__parse_x_y(task, "Snout")[0],
            head_y=cls.__parse_x_y(task, "Snout")[1],
            tail_x=cls.__parse_x_y(task, "Fork")[0],
            tail_y=cls.__parse_x_y(task, "Fork")[1],
            updated_at=cls.__parse_updated_time(task),
            json=json.loads(task.json()),
        )

    @staticmethod
    def __parse_x_y(task: Any, label: str) -> tuple[int, int]:
        label_value = [
            result
            for result in task.annotations[0]["result"]
            if label in result["value"]["keypointlabels"]
        ][0]

        log = logging.getLogger("HeadTailLabel")
        original_width = label_value["original_width"]
        original_height = label_value["original_height"]

        log.debug(
            "Parsed original height and width: %s, %s", original_width, original_height
        )

        x = int(round(label_value["value"]["x"] * original_width / 100))
        y = int(round(label_value["value"]["y"] * original_height / 100))

        log.debug("Parsed coordinates: x=%s, y=%s", x, y)

        return x, y

    @staticmethod
    def __parse_updated_time(task: Any) -> datetime | None:
        log = logging.getLogger("LaserLabel")
        updated_at = datetime.fromisoformat(task.annotations[0]["updated_at"])

        log.debug("Parsed updated_at: %s", updated_at)

        return updated_at
