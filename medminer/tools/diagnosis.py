import httpx
from smolagents import tool


@tool
def extract_diagnosis_data(
    data: list[dict],
    
) -> list[dict]:
    """
    Extract diagnosis data from the provided list of dictionaries.

    Args:
        data (list[dict]): A list of dictionaries containing medical data to save.
        All dictionaries must have the following keys:
        - patient_id: str, the ID of the patient.
        - diagnosis: str, the diagnosis of the patient.
        - diagnosis_corrected: str, the corrected and translated diagnosis of the patient.
        - year: int, the year of the diagnosis.
        - month: int, the month of the diagnosis.
    Returns:
         A message indicating where the data was saved.
    Example:
        >>> data = [
        ...     {"patient_id": 1, "diagnosis": "Heart Attack", "diagnosis_corrected": "Myocardial Infarction", "year": 2020, "month": 5},
        ...     {"patient_id": 2, "medication_name": "Paracetamol"},
        ... ]
        >>> extract_diagnosis_data("diagnosis", data)
    """
    return data


@tool
def get_diagnosis_info(
    diagnosis_names: str,
)