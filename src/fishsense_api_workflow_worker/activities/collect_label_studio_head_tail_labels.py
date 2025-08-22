import logging
from typing import List

from label_studio_sdk.client import LabelStudio
from temporalio import activity

from fishsense_api_workflow_worker.models.head_tail_label import HeadTailLabel


@activity.defn
async def collect_label_studio_head_tail_labels(
    label_studio_host: str, label_studio_api_key: str, head_tail_project_id: int
) -> List[HeadTailLabel]:
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

        labels.append(HeadTailLabel.from_task(task))

    return labels
