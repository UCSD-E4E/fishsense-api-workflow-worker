"""Worker for FishSense API Workflow"""

import asyncio
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

from fishsense_api_workflow_worker.activities.read_label_studio_laser_labels import (
    read_label_studio_laser_labels,
)
from fishsense_api_workflow_worker.config import configure_logging, settings
from fishsense_api_workflow_worker.workflows.read_label_studio_laser_labels import (
    ReadLabelStudioLaserLabelsWorkflow,
)

TASK_QUEUE_NAME = "fishsense_api_queue"


async def schedule_exists(client: Client, schedule_id: str) -> bool:
    """Check if a schedule exists."""
    schedules = await client.list_schedules()
    return any(s.id == schedule_id for s in schedules)


async def schedule_tasks(client: Client):
    """Schedule tasks for the worker."""

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
                    intervals=[ScheduleIntervalSpec(every=timedelta(seconds=5))]
                ),
                state=ScheduleState(),
            ),
        )


async def main():
    """Main entry point for the worker."""

    configure_logging()
    log = logging.getLogger()

    client = await Client.connect(f"{settings.temporal.host}:{settings.temporal.port}")

    worker = Worker(
        client,
        task_queue=TASK_QUEUE_NAME,
        workflows=[ReadLabelStudioLaserLabelsWorkflow],
        activities=[read_label_studio_laser_labels],
    )

    worker_task = worker.run()
    log.info("Worker started, scheduling tasks...")

    await schedule_tasks(client)
    await worker_task


def run():
    """Run the worker."""
    asyncio.run(main())
