from textwrap import dedent

from medminer.task import Task
from medminer.tools import save_csv

history_task = Task(
    name="history",
    prompt=dedent(
        """\
        Given a medical history of a patient, extract all given diagnoses and save all information as csv. The diagnosis should be translated to english. The medical history is usually in the format of a sentence or a paragraph. These are the steps you should follow to complete the task:
        1. extract a part of the text that contains a diagnosis. The diagnosis can be in any language. This is the diagnosis_reference column.
        2. translate the diagnoses to english if necessary and infer the diagnosis_translated column.
        3. Extract the relevant diagnosis as a string and loose everything that is not relevant. This is the diagnosis column.
        4. Extract the month and year of the medical history for that diagnosis. If not applicable, write an empty string.

        save the the following columns:
        - patient_id: The patient ID.
        - diagnosis_reference: The diagnosis of the medical history found in the text.
        - diagnosis_translated: The corrected diagnosis of the medical history, translated to english.
        - diagnosis: The extracted diagnosis.
        - month: The month of the medical history. if not applicable, write an empty string.
        - year: The year of the medical history. if not applicable, write an empty string.
        """
    ),
    tools=[save_csv],
)
