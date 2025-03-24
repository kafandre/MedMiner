from textwrap import dedent

from medminer.task import Task
from medminer.tools import save_csv

medication_task = Task(
    name="medication",
    prompt=dedent(
        """\
        Given a list of medications, save all medications for the patient as csv.
        If you detect any spelling mistakes of the medication name, please correct them.

        save the the following columns:
        - patient_id: The patient ID.
        - medication_name: The name of the medication in the document.
        - medication_name_corrected: The corrected name of the medication.
        - dose: The dose of the medication.
        - unit: The unit of the dose. if not applicable, write an empty string.
        - dosage_morning: The dose in the morning. if not applicable, write a 0.
        - dosage_noon: The dose in the noon. if not applicable, write a 0.
        - dosage_evening: The dose in the evening. if not applicable, write a 0.
        - dosage_night: The dose in the night. if not applicable, write a 0.
        - dosage_information: Additional information about the dosage. if not applicable, write an empty string.
        """
    ),
    tools=[save_csv],
)
