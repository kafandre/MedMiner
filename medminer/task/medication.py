from textwrap import dedent

from medminer.task import Task
from medminer.tools import extract_medication_data, get_medication_into, save_csv

medication_task = Task(
    name="medication",
    prompt=dedent(
        """\
        Given a list of medications, save all medications for the patient as csv.
        To complete the task make the following steps:
        1. extract all information defined in the columns below from the document. Infer the medication_name_corrected column.
        3. get the ATC code for all medications. Use the corrected name of the medications.
        4. save the medication information as csv with the columns defined below.

        Columns:
        - patient_id: The patient ID.
        - medication_name: The name of the medication in the document without dose, unit or additional information.
        - medication_name_corrected: Use the following format "Brand name or medication name (active ingredient)". e.g. "Aspirin (acetylsalicylic acid)".
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
    tools=[save_csv, get_medication_into, extract_medication_data],
)
