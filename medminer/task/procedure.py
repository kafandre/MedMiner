from textwrap import dedent

from medminer.task import Task
from medminer.tools import save_csv

procedure_task = Task(
    name="procedure",
    prompt=dedent(
        """\
        Given a icu stay protocol of a patient, save all information as csv.
        Make a column for each procedure.

        save the the following columns:
        - patient_id: The patient ID.
        - date: The date of the procedure. if not applicable, write an empty string.
        - procedure: The medical procedure.
        """
    ),
    tools=[save_csv],
)
