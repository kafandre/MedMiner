import httpx
from smolagents import tool


@tool
def extract_diagnosis_data(
    data: list[dict],
) -> list[dict]:
    """
    Adds extracted data to the task memory.
    
    Args:
        data: A list of dictionaries containing the data to save
        
            All dictionaries must have the following keys.
            - patient_id: The patient ID.
            - diagnosis_reference: The diagnosis of the medical history found in the text.
            - diagnosis_translated: The corrected diagnosis of the medical history, translated to english.
            - diagnosis: The extracted diagnosis.
            - month: The month of the medical history. if not applicable, write an empty string.
            - year: The year of the medical history. if not applicable, write an empty string.
    
    Returns:
        A message indicating where the data was saved.
        
    Example:
        >>> data = [
        ...     {"patient_id": 1, "diagnosis": "Myocardial Infarction"},
        ...     {"patient_id": 2, "diagnosis": "colon cancer"},
        ... ]
        >>> extract_diagnosis_data("diagnosis", data)
    """


@tool
def get_diagnosis_info(
    diagnosis_names: list[str],
) -> dict:
    pass
