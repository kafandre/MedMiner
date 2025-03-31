from textwrap import dedent

from medminer.task import Task
from medminer.tools import get_medication_into, save_csv

medication_task = Task(
    name="medication",
    prompt=dedent(
        """\
        Given a list of medications, save all medications for the patient as csv.
        To complete the task make the following steps:
        1. extract the following information from the document:
            - patient_id: The patient ID.
            - medication_name: The name of the medication in the document.
            - dose: The dose of the medication.
            - unit: The unit of the dose (e.g. ml, mg, ...).
            - dosage_morning: The dose in the morning.
            - dosage_noon: The dose in the noon.
            - dosage_evening: The dose in the evening.
            - dosage_night: The dose in the night.
            - dosage_information: Additional information about the dosage.
        2. correct the medication name if it is misspelled or use the brand name and print them out.
        3. get the ATC code of the now corrected medication name.
        4 save the medication information as csv.

        save the the following columns:
        - patient_id: The patient ID.
        - medication_name: The name of the medication in the document.
        - medication_name_corrected: The corrected name of the medication.
        - dose: The dose of the medication. this sould only contain the numeric value.
        - unit: The unit of the dose (e.g. ml, mg, ...). if not applicable, write an empty string.
        - dosage_morning: The dose in the morning. if not applicable, write a 0.
        - dosage_noon: The dose in the noon. if not applicable, write a 0.
        - dosage_evening: The dose in the evening. if not applicable, write a 0.
        - dosage_night: The dose in the night. if not applicable, write a 0.
        - dosage_information: Additional information about the dosage. if not applicable, write an empty string.
        - atc_id: The ATC code of the medication. if not applicable, write an empty string.
        - atc_name: The name of the ATC code. if not applicable, write an empty string.
        - atc_type: The type of the ATC code. if not applicable, write an empty string.
        """
    ),
    tools=[save_csv, get_medication_into],
)
