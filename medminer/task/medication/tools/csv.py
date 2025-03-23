from csv import DictWriter
from pathlib import Path

from smolagents import tool


@tool
def save_csv(
    patiend_id: str,
    medication_name: str,
    dose: float,
    unit: str,
    dosage_morning: float,
    dosage_noon: float,
    dosage_evening: float,
    dosage_night: float,
    dosage_information: str,
) -> str:
    """
    Saves a medication to a csv file.

    Args:
        patiend_id: The patient ID.
        medication_name: The name of the medication.
        dose: The dose of the medication.
        unit: The unit of the dose.
        dosage_morning: The dose in the morning.
        dosage_noon: The dose in the noon.
        dosage_evening: The dose in the evening.
        dosage_night: The dose in the night.
        dosage_information: Additional information about the dosage.
    """
    fieldnames = [
        "patiend_id",
        "medication_name",
        "dose",
        "unit",
        "dosage_morning",
        "dosage_noon",
        "dosage_evening",
        "dosage_night",
        "dosage_information",
    ]

    file_path = Path.cwd() / "result" / "medications.csv"
    if not file_path.parent.exists():
        file_path.parent.mkdir(parents=True)

    with open(file_path, "a") as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames)

        if file_path.exists() and file_path.stat().st_size == 0:
            writer.writeheader()

        writer.writerow(
            {
                "patiend_id": patiend_id,
                "medication_name": medication_name,
                "dose": dose,
                "unit": unit,
                "dosage_morning": dosage_morning,
                "dosage_noon": dosage_noon,
                "dosage_evening": dosage_evening,
                "dosage_night": dosage_night,
                "dosage_information": dosage_information,
            }
        )

    return f"Saved medication {medication_name} for patient {patiend_id} to {file_path}"
