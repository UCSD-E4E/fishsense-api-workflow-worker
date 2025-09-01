"""Activity to insert laser labels into PostgreSQL database."""

from typing import List

from sqlmodel.ext.asyncio.session import AsyncSession
from temporalio import activity

from fishsense_api_workflow_worker.database import Database
from fishsense_api_workflow_worker.models.laser_label import LaserLabel


@activity.defn
async def insert_laser_labels_into_postgres(labels: List[LaserLabel]):
    # pylint: disable=duplicate-code
    """Activity to insert laser labels into PostgreSQL database."""

    database = Database()
    async with AsyncSession(database.engine) as conn:
        for label in labels:
            if activity.is_cancelled():
                conn.rollback()
                return

            existing_label = await database.select_laser_label_by_task_id(
                label.label_studio_task_id
            )
            if existing_label:
                label.id = existing_label.id

            database.insert_or_update_laser_label(label, session=conn)

        conn.commit()
