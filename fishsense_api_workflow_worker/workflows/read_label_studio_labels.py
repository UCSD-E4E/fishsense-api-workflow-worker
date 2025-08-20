from temporalio import workflow


@workflow.defn
class ReadLabelStudioLabelsWorkflow:
    @workflow.run
    async def run(self) -> str:
        return "Hello World!"
