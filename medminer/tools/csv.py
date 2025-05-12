"""
This module contains tools for saving data to a csv file.
"""

from csv import DictWriter
from itertools import chain
from pathlib import Path

from smolagents import Tool

from medminer.tools.settings import ToolSetting, ToolSettingMixin


class CSVTool(ToolSettingMixin, Tool):
    """A tool for saving data to a csv file."""

    name = "save_csv"
    description = "Saves data to a csv file."
    inputs = {
        "task_name": {"type": "string", "description": "The name of the task."},
        "data": {
            "type": "array",
            "items": {"type": "object"},
            "description": "A list of dictionaries containing the data to save. All dictionaries must have the same keys.",
        },
    }
    output_type = "string"

    # Tool settings
    settings = [
        ToolSetting(id="session_id", label="Session ID", type=str),
        ToolSetting(id="task_name", label="Task Name", type=str),
        ToolSetting(id="base_dir", label="Base Directory", type=Path),
    ]
    session_id: str
    task_name: str
    base_dir: Path

    def forward(
        self,
        task_name: str,
        data: list[dict],
    ) -> str:
        """
        Saves data to a csv file.

        Args:
            task_name: The name of the task.
            data: A list of dictionaries containing the data to save.
                All dictionaries must have the same keys.

        Returns:
            A message indicating where the data was saved.

        Example:
            >>> data = [
            ...     {"patient_id": 1, "medication_name": "Aspirin"},
            ...     {"patient_id": 2, "medication_name": "Paracetamol"},
            ... ]
            >>> save_csv("medication", data)
            "Saved data for task medication to /path/to/result/medication.csv"
        """
        if isinstance(data, list) and not data:
            return "No data to save."

        # small hack to get all keys from all dictionaries to have all possible columns
        fieldnames = dict.fromkeys(chain.from_iterable([d.keys() for d in data])).keys()
        file_path = self.base_dir / self.session_id / f"{self.task_name}.csv"
        if not file_path.parent.exists():
            file_path.parent.mkdir(parents=True)

        with open(file_path, "a") as csvfile:
            writer = DictWriter(csvfile, fieldnames=fieldnames)

            if file_path.exists() and file_path.stat().st_size == 0:
                writer.writeheader()

            for row in data:
                writer.writerow(row)

        return f"Saved data for task {task_name} to {file_path}"
