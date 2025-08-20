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

from fishsense_api_workflow_worker.workflows.read_label_studio_labels import (
    ReadLabelStudioLabelsWorkflow,
)

TASK_QUEUE_NAME = "fishsense_api_queue"


async def schedule_tasks(client: Client):
    await client.create_schedule(
        "read-label-studio-labels-schedule",
        Schedule(
            action=ScheduleActionStartWorkflow(
                ReadLabelStudioLabelsWorkflow.run,
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
    client = await Client.connect("localhost:7233")

    worker = Worker(
        client,
        task_queue=TASK_QUEUE_NAME,
        workflows=[ReadLabelStudioLabelsWorkflow],
        activities=[],
    )

    worker_task = worker.run()

    await schedule_tasks(client)
    await worker_task
