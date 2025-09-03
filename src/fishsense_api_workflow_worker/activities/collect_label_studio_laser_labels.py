"""Activity to collect laser labels from Label Studio."""

import logging
from typing import List

from label_studio_sdk.client import LabelStudio
from temporalio import activity

from fishsense_api_workflow_worker.database import Database
from fishsense_api_workflow_worker.models.laser_label import LaserLabel


@activity.defn
async def collect_label_studio_laser_labels(
    label_studio_host: str, label_studio_api_key: str, database_url: str, laser_project_id: int
) -> List[LaserLabel]:
    # pylint: disable=duplicate-code

    """Activity to collect labels from Label Studio."""

    log = logging.getLogger("read_label_studio_labels")

    log.debug("Label Studio server location: %s", label_studio_host)
    log.info("Collecting laser labels from Label Studio project: %s", laser_project_id)
    client = LabelStudio(
        base_url=f"https://{label_studio_host}", api_key=label_studio_api_key
    )

    database = Database(database_url)

    labels: List[LaserLabel] = []
    for task in client.tasks.list(project=laser_project_id):
        if activity.is_cancelled():
            log.warning("Activity was cancelled")
            return labels

        if not task.annotations or not task.annotations[0]["result"]:
            continue

        existing_labels = await database.select_laser_label_by_task_id(task.id)

        user = await database.select_user_by_email(
            task.annotations[0]["created_username"].split(",")[0].strip()
        )

        laser_label = LaserLabel.from_task(task)
        laser_label.image_id = existing_labels.image_id if existing_labels else None
        laser_label.user_id = user.id if user else None

        labels.append(laser_label)

    return labels
