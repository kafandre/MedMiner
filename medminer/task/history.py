from textwrap import dedent

from medminer.task import Task
from medminer.tools import extract_diagnosis_data, get_diagnosis_info, save_csv

history_task = Task(
    name="history",
    prompt=dedent(
        """\
        Given a medical history of a patient, extract all given diagnoses and save all information as csv. The diagnosis should be translated to english. The medical history is usually in the format of a sentence or a paragraph. Every diagnosis should have a single row, if there are multiple diagnosis that can be extracted from a single piece of text, split them up. These are the steps you should follow to complete the task:
        1. extract a part of the text that contains a diagnosis. The diagnosis can be in any language. This is the diagnosis_reference column.
        2. translate the diagnoses to english if necessary and infer the diagnosis_translated column.
        3. Extract the relevant diagnosis as a string and loose everything that is not relevant. This is the diagnosis column.
        4. Extract the month and year of the medical history for that diagnosis. If not applicable, write an empty string.

        Example 1:
        Input: "schwere Herzinsuffizienz, 2. Grad, NYHA II, ED 07/2023"
        Output: [{"patient_id": 1, "diagnosis_reference": "schwere chronische Herzinsuffizienz, 2. Grad, NYHA II", "diagnosis_translated": "severe chronic heart failure, 2nd degree, NYHA II", "diagnosis": "chronic heart failure", "month": "7", "year": "2023"}]

        Example 2:
        Input: "Myocardial Infarction"
        Output: [{"patient_id": 2, "diagnosis_reference": "Myocardial Infarction", "diagnosis_translated": "Myocardial Infarction", "diagnosis": "Myocardial Infarction", "month": "", "year": ""}]        

        Example 3:
        Input: "Lungenteilresektion rechts bei Lungenmetastasen eines Kolonkarzinoms, 2023-07-01"
        Output: [
            {"patient_id": 3, "diagnosis_reference": "Lungenteilresektion rechts bei Lungenmetastasen eines Kolonkarzinoms", "diagnosis_translated": "Lung resection due to lung metastases of colon cancer", "diagnosis": "colon cancer", "month": "7", "year": "2023"},
            {"patient_id": 3, "diagnosis_reference": "Lungenteilresektion rechts bei Lungenmetastasen eines Kolonkarzinoms", "diagnosis_translated": "Lung resection due to lung metastases of colon cancer", "diagnosis": "lung metastasis", "month": "7", "year": "2023"}
        ]

        save the the following columns:
        - patient_id: The patient ID.
        - diagnosis_reference: The diagnosis of the medical history found in the text.
        - diagnosis_translated: The corrected diagnosis of the medical history, translated to english.
        - diagnosis: The extracted diagnosis.
        - month: The month of the medical history. if not applicable, write an empty string.
        - year: The year of the medical history. if not applicable, write an empty string.
        """
    ),
    tools=[save_csv, extract_diagnosis_data, get_diagnosis_info],
)
