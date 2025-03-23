from textwrap import dedent

from medminer.task import Task
from medminer.task.medication.tools import save_csv

medication_task = Task(
    name="medication",
    prompt=dedent(
        """
        Given a list of medications, save all medications for the patient as csv.
        """
    ),
    tools=[save_csv],
)
