from textwrap import dedent

from medminer.task import Task
from medminer.tools import save_csv

history_task = Task(
    name="history",
    prompt=dedent(
        """\
        Given a medical history of a patient, save all information as csv.

        save the the following columns:
        - patient_id: The patient ID.
        - date: The date of the medical history. if not applicable, write an empty string.
        - year: The year of the medical history. if not applicable, write an empty string.
        - diagnosis: The diagnosis of the medical history.
        """
    ),
    tools=[save_csv],
)
