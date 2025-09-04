"""Activity to sync laser labels from Label Studio to the database."""

from label_studio_sdk.client import LabelStudio
from sqlmodel.ext.asyncio.session import AsyncSession
from temporalio import activity

from fishsense_api_workflow_worker.database import Database
from fishsense_api_workflow_worker.models.laser_label import LaserLabel


@activity.defn
async def sync_label_studio_laser_labels(
    label_studio_host: str,
    label_studio_api_key: str,
    database_url: str,
    laser_project_id: int,
) -> None:
    # pylint: disable=duplicate-code
    """Collect laser labels from Label Studio and insert them into the database."""

    log = activity.logger

    log.debug("Label Studio server location: %s", label_studio_host)
    log.info("Collecting laser labels from Label Studio project: %s", laser_project_id)
    client = LabelStudio(
        base_url=f"https://{label_studio_host}", api_key=label_studio_api_key
    )

    database = Database(database_url)

    async with AsyncSession(database.engine) as conn:
        for task in client.tasks.list(project=laser_project_id):
            if activity.is_cancelled():
                log.warning("Activity was cancelled")
                await conn.rollback()
                return

            if not task.annotations:
                continue

            existing_label = await database.select_laser_label_by_task_id(
                task.id, session=conn
            )

            laser_label = LaserLabel.from_task(task)
            laser_label.image_id = existing_label.image_id if existing_label else None
            laser_label.user_id = user.id if user else None

            user = await database.select_user_by_email(
                task.annotations[0]["created_username"].split(",")[0].strip(),
                session=conn,
            )

            if existing_label:
                laser_label.id = existing_label.id

            await database.insert_or_update_laser_label(laser_label, session=conn)

        await conn.commit()
