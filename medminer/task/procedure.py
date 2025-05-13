"""
This module contains the ProcedureTask class, which is responsible for extracting and processing medical procedures from text data.
"""

from textwrap import dedent

from medminer.task import Task, register_task
from medminer.tools import SNOMEDTool
from medminer.tools.csv import CSVTool
from medminer.tools.procedure import extract_procedure_data


@register_task
class ProcedureTask(Task):
    name = "procedure"
    verbose_name = "Procedures"
    prompt = dedent(
        """\
        Given a medical course of a patient, extract all given procedures and save all information as csv. The procedures can be in any language. The medical course is usually in the format of bullet points. Every procedure should have a single row, if there are multiple procedures that can be extracted from a single piece of text, split them up. These are the steps you should follow to complete the task:

        To complete the task take the following steps for each single procedure::
        1. Extract the procedure from the text. The procedure can be in any language. This is the `procedure_reference` column.
        2. If the procedure name is not in English, translate it to English and infer the `procedure_corrected` column. Correct any misspellings in the process. Change abbreviations to full words. For example, "CT" should be changed to "Computed Tomography".
        3. Extract the relevant procedure as a search term. Separate the words with a space. Remove unnecessary stop words. Make sure spelling is correct. Make sure you're only searching for one procedure at the time, This is the `procedure_search` column.
        5. Extract the date of the procedure. If not applicable, write an empty string. This is the `year`, `month` and `day` column. Write an empty string if not applicable.

        After you extracted all relevant procedures go through each of the procedure_search_terms and search for the SNOMED CT ID and FSN.
        The SNOMED CT ID is a unique identifier for the procedure in the SNOMED CT database.
        The FSN is a fully specified name (FSN) of the procedure in SNOMED CT.
        Use the `search_snomed_procedures` tool to find SNOMED CT concepts to finde the information by following these steps:
        - supply the `procedure_search` term to the `term` parameter of the tool.
        - supply synonyms (e.g. {"Cranial": "Head"}) for the words in the search term to the `synonyms` parameter of the tool. if there are no synonyms, write an empty dict.
        - supply additional keywords (e.g. CT) to the `keywords` parameter of the tool. If there are no additional keywords, write an empty list.
        If possible add synonyms for words in the search term and additional keywords to the tool call.
        You will get back a list of dictionaries with the following keys: ids and fsn.
        Compare the extracted information with the returned descriptions from the snomed server and choose the returned concept that matches the searched term the closest.
        Make sure not do add or loose any detail. If there are no codes, write an empty string. This is the `snomed_id` and `snomed_fsn` columns.

        Example 1:
        Input: "Colonoscopy performed on 2023-04-15"
        Output: [
            {"patient_id": 1, "procedure_reference": "Colonoscopy performed on 2023-04-15", "procedure_corrected": "Colonoscopy", "procedure_search": "Colonoscopy",
            "year": 2023, "month": 4, "day": 15, "snomed_id": "73761001", "snomed_fsn": "Colonoscopy (procedure)"},

        ]

        Example 2:
        Input: "Gastroscopy and biopsy conducted on 2023-03-10"
        Output: [
            {"patient_id": 2, "procedure_reference": "Gastroscopy and biopsy conducted on 2023-03-10", "procedure_corrected": "Gastroscopy", "procedure_search": "Gastroscopy",
            "year": 2023, "month": 3, "day": 10, "snomed_id": "274441001", "snomed_fsn": "Gastroscopy (procedure)"},
            {"patient_id": 2, "procedure_reference": "Gastroscopy and biopsy conducted on 2023-03-10", "procedure_corrected": "Biopsy", "procedure_search": "Biopsy",
            "year": 2023, "month": 3, "day": 10, "snomed_id": "118234003", "snomed_fsn": "Biopsy (procedure)"},
        ]

        Example 3:
        Input: "CT scan of the abdomen on 05-20"
        Output: [
            {"patient_id": 3, "procedure_reference": "CT scan of the abdomen on 05-20", "procedure_corrected": "Computed Tomography scan of the abdomen", "procedure_search": "Computed Tomography scan of the abdomen",
            "year": "", "month": 5, "day": 20, "snomed_id": "938264203", "snomed_fsn": "Computed Tomography scan of the abdomen (procedure)"},
        ]

        Columns:
        - patient_id: The patient ID.
        - procedure_reference: The original text containing the procedure.
        - procedure_corrected: Translate the procedures to English if necessary and infer the column. Change abbreviations to full words. For example, "CT" should be changed to "Computed Tomography".
        - procedure_search: The relevant procedure as a string. Separate the words with a space.
        - year: The year of the procedure.
        - month: The month of the procedure.
        - day: The day of the procedure.

        - snomed_id: The SNOMED CT ID of the procedure.
        - snomed_fsn: The fully specified name (FSN) of the procedure in SNOMED CT.
        """
    )
    tools = [CSVTool, SNOMEDTool, extract_procedure_data]
