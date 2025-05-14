from textwrap import dedent, indent

from medminer.task import Task, register_task
from medminer.tools import CSVTool, get_rxcui, get_va
from medminer.tools.settings import ToolSetting


@register_task
class BooleanTask(Task):
    name = "boolean"
    verbose_name = "Filter"
    prompt = dedent(
        """
        Given a medical information of a patient, extract all patients which information match a given filter query. These are the steps you should follow to complete the task:

        1. Check if the medical information of the patient matches the filter query.
        2. save the information as csv with the columns defined below.
        3a. If the patient information contains a list of medications, extract the medications from the text. The medication can be in any language.
        3b. If the medication name is not in english, translate it to english and infer the name. Correct any misspellings in the process. Use the following format "Brand name or medication name (active ingredient)". e.g. "Aspirin (acetylsalicylic acid)".
        3c. get the RXCUI for all medications. Use the active ingredient of the medications. If there are multiple RXCUI codes, choose the one that fits the best to the translated medication. Usually, the first candidate with a score of 1 is the best choice, but you can decide otherwise if you have reasonable grounds for another decision. If there are no codes, write an empty string.
        3d. get the VA code and information for all medications. Use the rxcui of the medications.
        3e. look if the VA code of one of the medications matches the filter query.
        4. If the patient information contains a list of procedures, extract the procedures from the text and look if the procedure name matches the filter query.
        5. If the patient information contains a list of diagnoses, extract the diagnoses from the text and look if the diagnosis name matches the filter query.
        6. Save every patient only once. If the patient information not matches the filter query, save the patient information as well but set the patient_filter to false.

        Example 1:
            Query: "return all patients which where given antibiotics"
            Input: "Patient 1: Doxycyclin 200 mg  0-1-0"
            Output: [
                {"patient_id": 1, "patient_filter": True, "patient_information": "Doxycyclin 200 mg  0-1-0", "filter_reference": "Doxycyclin"},
            ]

        save the following columns:
        - patient_id: The patient ID.
        - patient_filter: True if the patient information matches the filter query, false otherwise.
        - patient_information: The medical information of the patient that matched the query.
        - filter_reference: The part of the text that was relevant for your decision in filtering. If not applicable, write an empty string.
        """
    )
    tools = [CSVTool, get_rxcui, get_va]

    @classmethod
    def settings(cls) -> list[ToolSetting]:
        settings = super().settings()
        settings.append(ToolSetting(id="boolean_query", label="Filter Query", type=str))
        return settings

    def _buidl_prompt(self, data: str) -> str:
        return dedent(
            f"""\
            Task name: {self.name}
            Prompt: \n{indent(self.prompt, " " * 4 * 5)}

            Filter query: {self._settings.get("boolean_query", "")}

            {"-" * 80}
            Data: \n{indent(data, " " * 4 * 5)}
            """
        )
