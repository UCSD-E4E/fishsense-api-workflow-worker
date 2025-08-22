import logging
from typing import Any
from urllib.parse import urlparse

from pydantic import BaseModel


class HeadTailLabel(BaseModel):
    task_id: int
    checksum: str
    head_x: int
    head_y: int
    tail_x: int
    tail_y: int

    @classmethod
    def from_task(cls, task: Any) -> "HeadTailLabel":
        """Create a HeadTailLabel instance from a Label Studio task."""

        log = logging.getLogger("HeadTailLabel")
        log.debug("Initializing HeadTailLabel with task ID: %s", task.id)

        return cls(
            task_id=task.id,
            checksum=cls.__parse_checksum(task),
            head_x=cls.__parse_x_y(task, "Snout")[0],
            head_y=cls.__parse_x_y(task, "Snout")[1],
            tail_x=cls.__parse_x_y(task, "Fork")[0],
            tail_y=cls.__parse_x_y(task, "Fork")[1],
        )

    @staticmethod
    def __parse_checksum(task: Any) -> str:
        log = logging.getLogger("HeadTailLabel")
        checksum = urlparse(task.data["img"]).path.split("/")[-1]

        log.debug("Parsed checksum: %s", checksum)

        return checksum

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

        x = int(round(label_value["value"]["x"] * original_width))
        y = int(round(label_value["value"]["y"] * original_height))

        log.debug("Parsed coordinates: x=%s, y=%s", x, y)

        return x, y
