"""Workflow definition for reading laser labels from Label Studio."""

from temporalio import workflow


@workflow.defn
class ReadLabelStudioLaserLabelsWorkflow:
    """Workflow for reading laser labels from Label Studio."""

    # pylint: disable=too-few-public-methods
    @workflow.run
    async def run(self) -> str:
        """Run the workflow to read laser labels."""

        return "Hello World!"
