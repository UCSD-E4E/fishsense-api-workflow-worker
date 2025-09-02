"""Worker for FishSense API Workflow"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging
from datetime import timedelta

from temporalio.client import (
    Client,
    Schedule,
    ScheduleActionStartWorkflow,
    ScheduleIntervalSpec,
    ScheduleSpec,
    ScheduleState,
)
from temporalio.worker import Worker

from fishsense_api_workflow_worker.activities.collect_label_studio_head_tail_labels import (
    collect_label_studio_head_tail_labels,
)
from fishsense_api_workflow_worker.activities.collect_label_studio_laser_labels import (
    collect_label_studio_laser_labels,
)
from fishsense_api_workflow_worker.activities.collect_label_studio_users import (
    collect_label_studio_users,
)
from fishsense_api_workflow_worker.activities.insert_head_tail_labels_into_postgres import (
    insert_head_tail_labels_into_postgres,
)
from fishsense_api_workflow_worker.activities.insert_laser_labels_into_postgres import (
    insert_laser_labels_into_postgres,
)
from fishsense_api_workflow_worker.activities.insert_users_into_postgres import (
    insert_users_into_postgres,
)
from fishsense_api_workflow_worker.config import configure_logging, settings
from fishsense_api_workflow_worker.database import Database
from fishsense_api_workflow_worker.workflows.read_label_studio_head_tail_labels import (
    ReadLabelStudioHeadTailLabelsWorkflow,
)
from fishsense_api_workflow_worker.workflows.read_label_studio_laser_labels import (
    ReadLabelStudioLaserLabelsWorkflow,
)

TASK_QUEUE_NAME = "fishsense_api_queue"


async def schedule_exists(client: Client, schedule_id: str) -> bool:
    """Check if a schedule exists."""
    schedules = await client.list_schedules()
    async for s in schedules:
        if s.id == schedule_id:
            return True

    # If we reach here, no schedule with the given ID was found
    logging.info("No schedule found with ID: %s", schedule_id)


async def schedule_read_label_studio_laser_label_workflows(client: Client):
    """Schedule workflows to read laser labels from Label Studio."""
    for laser_project_id in settings.label_studio.laser_project_ids:
        schedule_id = f"read-label-studio-laser-labels-schedule-{laser_project_id}"

        if await schedule_exists(client, schedule_id):
            logging.info("Schedule %s already exists, skipping...", schedule_id)
            continue

        await client.create_schedule(
            schedule_id,
            Schedule(
                action=ScheduleActionStartWorkflow(
                    ReadLabelStudioLaserLabelsWorkflow.run,
                    args=(
                        settings.label_studio.host,
                        settings.label_studio.api_key,
                        laser_project_id,
                    ),
                    id=f"read-label-studio-laser-labels-workflow-{laser_project_id}",
                    task_queue=TASK_QUEUE_NAME,
                ),
                spec=ScheduleSpec(
                    intervals=[ScheduleIntervalSpec(every=timedelta(hours=1))]
                ),
                state=ScheduleState(),
            ),
        )


async def schedule_read_label_studio_head_tail_label_workflows(client: Client):
    """Schedule workflows to read head-tail labels from Label Studio."""
    for head_tail_project_id in settings.label_studio.head_tail_project_ids:
        schedule_id = (
            f"read-label-studio-head-tail-labels-schedule-{head_tail_project_id}"
        )

        if await schedule_exists(client, schedule_id):
            logging.info("Schedule %s already exists, skipping...", schedule_id)
            continue

        await client.create_schedule(
            schedule_id,
            Schedule(
                action=ScheduleActionStartWorkflow(
                    ReadLabelStudioHeadTailLabelsWorkflow.run,
                    args=(
                        settings.label_studio.host,
                        settings.label_studio.api_key,
                        head_tail_project_id,
                    ),
                    id=f"read-label-studio-head-tail-labels-workflow-{head_tail_project_id}",
                    task_queue=TASK_QUEUE_NAME,
                ),
                spec=ScheduleSpec(
                    intervals=[ScheduleIntervalSpec(every=timedelta(hours=1))]
                ),
                state=ScheduleState(),
            ),
        )


async def schedule_workflows(client: Client):
    """Schedule workflows for the worker."""

    async with asyncio.TaskGroup() as tg:
        tg.create_task(schedule_read_label_studio_laser_label_workflows(client))
        tg.create_task(schedule_read_label_studio_head_tail_label_workflows(client))


async def main():
    """Main entry point for the worker."""

    configure_logging()
    log = logging.getLogger()

    database = Database()
    await database.init_database()

    client = await Client.connect(f"{settings.temporal.host}:{settings.temporal.port}")

    with ThreadPoolExecutor(max_workers=8) as executor:
        worker = Worker(
            client,
            task_queue=TASK_QUEUE_NAME,
            workflows=[
                ReadLabelStudioLaserLabelsWorkflow,
                ReadLabelStudioHeadTailLabelsWorkflow,
            ],
            activity_executor=executor,
            activities=[
                insert_laser_labels_into_postgres,
                insert_head_tail_labels_into_postgres,
                insert_users_into_postgres,
                collect_label_studio_laser_labels,
                collect_label_studio_head_tail_labels,
                collect_label_studio_users,
            ],
        )

        worker_task = worker.run()
        log.info("Worker started, scheduling workflows...")

        await schedule_workflows(client)
        await worker_task


def run():
    """Run the worker."""
    asyncio.run(main())
