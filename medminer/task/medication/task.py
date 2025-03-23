from textwrap import dedent

from medminer.task import Task

medication_task = Task(
    name="medication",
    prompt=dedent(
        """
        Given a list of medications, return the medication with the highest dose.
        """
    ),
    tools=[],
)
