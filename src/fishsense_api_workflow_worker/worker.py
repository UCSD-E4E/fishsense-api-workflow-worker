"""Worker for FishSense API Workflow"""

import asyncio
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

from fishsense_api_workflow_worker.config import settings
from fishsense_api_workflow_worker.workflows.read_label_studio_laser_labels import (
    ReadLabelStudioLaserLabelsWorkflow,
)

TASK_QUEUE_NAME = "fishsense_api_queue"


async def schedule_tasks(client: Client):
    """Schedule tasks for the worker."""

    await client.create_schedule(
        "read-label-studio-laser-labels-schedule",
        Schedule(
            action=ScheduleActionStartWorkflow(
                ReadLabelStudioLaserLabelsWorkflow.run,
                *[],
                id="read-label-studio-workflow",
                task_queue=TASK_QUEUE_NAME,
            ),
            spec=ScheduleSpec(
                intervals=[ScheduleIntervalSpec(every=timedelta(seconds=1))]
            ),
            state=ScheduleState(),
        ),
    )


async def main():
    """Main entry point for the worker."""

    client = await Client.connect(f"{settings.temporal.host}:{settings.temporal.port}")

    worker = Worker(
        client,
        task_queue=TASK_QUEUE_NAME,
        workflows=[ReadLabelStudioLaserLabelsWorkflow],
        activities=[],
    )

    worker_task = worker.run()

    await schedule_tasks(client)
    await worker_task


def run():
    """Run the worker."""
    asyncio.run(main())
