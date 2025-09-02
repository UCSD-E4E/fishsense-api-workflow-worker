"""Collects head-tail labels from Label Studio."""

import logging
from typing import List

from label_studio_sdk.client import LabelStudio
from temporalio import activity

from fishsense_api_workflow_worker.database import Database
from fishsense_api_workflow_worker.models.head_tail_label import HeadTailLabel


@activity.defn
async def collect_label_studio_head_tail_labels(
    label_studio_host: str, label_studio_api_key: str, head_tail_project_id: int
) -> List[HeadTailLabel]:
    # pylint: disable=duplicate-code

    """Activity to collect head-tail labels from Label Studio."""

    log = logging.getLogger("collect_label_studio_head_tail_labels")

    log.debug("Label Studio server location: %s", label_studio_host)
    log.info(
        "Collecting head-tail labels from Label Studio project: %s",
        head_tail_project_id,
    )
    client = LabelStudio(
        base_url=f"https://{label_studio_host}", api_key=label_studio_api_key
    )

    database = Database()

    labels: List[HeadTailLabel] = []
    for task in client.tasks.list(project=head_tail_project_id):
        if activity.is_cancelled():
            log.warning("Activity was cancelled")
            return labels

        if not task.annotations or not task.annotations[0]["result"]:
            continue

        keypoint_labels = {
            label
            for result in task.annotations[0]["result"]
            for label in result["value"]["keypointlabels"]
        }

        if len(keypoint_labels) != 2:
            log.warning(
                "Task %s has %d keypoint labels, expected 2. Skipping task.",
                task.id,
                len(keypoint_labels),
            )
            continue

        existing_labels = await database.select_head_tail_labels_by_task_id(task.id)

        user = await database.select_user_by_email(
            task.annotations[0]["created_username"].split(",")[0].strip()
        )

        headtail_label = HeadTailLabel.from_task(task)
        headtail_label.image_id = existing_labels.image_id if existing_labels else None
        headtail_label.user_id = user.id if user else None

        labels.append(headtail_label)

    return labels
