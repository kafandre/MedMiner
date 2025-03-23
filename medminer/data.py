from dataclasses import dataclass
from textwrap import dedent


@dataclass
class Document:
    patient_id: str
    text: str

    @property
    def content(self) -> str:
        return dedent(
            f"""
            Patiend: {self.patient_id}

            {self.text}
        """
        )
