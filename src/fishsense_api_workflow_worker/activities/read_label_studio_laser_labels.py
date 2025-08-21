"""Activity to read laser labels from Label Studio."""

import logging
from typing import List

from label_studio_sdk.client import LabelStudio
from temporalio import activity

from fishsense_api_workflow_worker.models.laser_label import LaserLabel


@activity.defn
async def read_label_studio_laser_labels(
    label_studio_host: str, label_studio_api_key: str, laser_project_id: int
) -> List[LaserLabel]:
    """Activity to read labels from Label Studio."""

    log = logging.getLogger("read_label_studio_labels")

    log.debug("Label Studio server location: %s", label_studio_host)
    log.info("Reading laser labels from Label Studio project: %s", laser_project_id)
    client = LabelStudio(
        base_url=f"https://{label_studio_host}", api_key=label_studio_api_key
    )

    labels: List[LaserLabel] = []
    for task in client.tasks.list(project=laser_project_id):
        if activity.is_cancelled():
            log.warning("Activity was cancelled")
            return labels

        if not task.annotations or not task.annotations[0]["result"]:
            continue

        labels.append(LaserLabel.from_task(task))

    return labels
