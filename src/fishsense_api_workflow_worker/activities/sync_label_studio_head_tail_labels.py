"""Activity to sync head-tail labels from Label Studio to the database."""

from label_studio_sdk.client import LabelStudio
from sqlmodel.ext.asyncio.session import AsyncSession
from temporalio import activity

from fishsense_api_workflow_worker.database import Database
from fishsense_api_workflow_worker.models.head_tail_label import HeadTailLabel


@activity.defn
async def sync_label_studio_head_tail_labels(
    label_studio_host: str,
    label_studio_api_key: str,
    database_url: str,
    head_tail_project_id: int,
) -> None:
    # pylint: disable=duplicate-code
    """Collect head-tail labels from Label Studio and insert them into the database."""

    log = activity.logger

    log.debug("Label Studio server location: %s", label_studio_host)
    log.info(
        "Collecting head-tail labels from Label Studio project: %s",
        head_tail_project_id,
    )
    client = LabelStudio(
        base_url=f"https://{label_studio_host}", api_key=label_studio_api_key
    )

    database = Database(database_url)
    async with AsyncSession(database.engine) as conn:
        for task in client.tasks.list(project=head_tail_project_id):
            if activity.is_cancelled():
                log.warning("Activity was cancelled")
                await conn.rollback()
                return

            if not task.annotations:
                continue

            existing_label = await database.select_head_tail_labels_by_task_id(
                task.id, session=conn
            )

            if task.annotations[0]["result"]:
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

            user = await database.select_user_by_email(
                task.annotations[0]["created_username"].split(",")[0].strip(),
                session=conn,
            )

            headtail_label = HeadTailLabel.from_task(task)
            headtail_label.image_id = (
                existing_label.image_id if existing_label else None
            )
            headtail_label.user_id = user.id if user else None

            if existing_label:
                headtail_label.id = existing_label.id

            await database.insert_or_update_head_tail_label(
                headtail_label, session=conn
            )

        await conn.commit()
