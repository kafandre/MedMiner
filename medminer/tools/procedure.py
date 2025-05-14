"""
This module contains various tools for extracting and processing medical data.
"""
from __future__ import annotations

from itertools import combinations
from typing import Iterator

import httpx
from smolagents import Tool, tool

from medminer.tools.settings import ToolSetting, ToolSettingMixin


@tool
def extract_procedure_data(
    data: list[dict],
) -> list[dict]:
    """
    Adds extracted data to the task memory.

    Args:
        data: A list of dictionaries containing the data to save.
            All dictionaries must have the following keys.
            - patient_id: The patient ID.
            - date: The date of the procedure. If not applicable, write an empty string.
            - procedure_reference: The original text containing the procedure. Use only the procedure text.
            - procedure_corrected: Translate the procedures to English if necessary and infer the column. Change abbreviations to full words. For example, "CT" should be changed to "Computed Tomography".
            - procedure_search: The relevant procedure as a string. Remove everything that is not relevant. Separate the words with a space.
            - procedure: The relevant procedure as a string. Remove everything that is not relevant.
    Returns:
        A message indicating where the data was saved.

    Example:
        >>> data = [
        ...     {"patient_id": 1, ...},
        ...     {"patient_id": 2, ...},
        ... ]
        >>> extract_procedure_data(data)
    """
    return data


class SNOMEDTool(ToolSettingMixin, Tool):
    """A tool for searching SNOMED CT concepts."""

    name = "search_snomed_procedures"
    description = "Search SNOMED CT for procedures matching the given term."
    inputs = {
        "term": {"type": "string", "description": "The search term (written out text) to query."},
        "synonyms": {
            "type": "object",
            "items": {"type": "string"},
            "description": "A dictionary of synonyms for the words in the search term. e.g. {'Cranial': 'Head'}",
        },
        "keywords": {
            "type": "array",
            "items": {"type": "string"},
            "description": "A list of keywords to search for in addition to the search term e.g. ['CT', 'MRI']",
        },
    }
    output_type = "array"
    settings = [
        ToolSetting(id="base_url", label="Base URL", type=str),
        ToolSetting(id="edition", label="Edition", type=str),
    ]
    base_url: str
    edition: str

    def _build_ecl_queries(
        self,
        term: str,
        synonyms: dict[str, str],
        keywords: list[str],
    ) -> Iterator[str]:
        """
        Build the ECL query for SNOMED CT.

        Args:
            term: The search term to query.
            synonyms: A dictionary of synonyms for the words in the search term.
            keywords: A list of keywords to search for.

        Returns:
            The ECL query string.
        """

        procedure_definition = "< 71388002|Procedure|"

        yield f'{procedure_definition} {{{{ term = "{term}"}}}}'

        words = term.split(" ")
        if synonyms:
            syn_terms = [
                f'term = ("{word}" "{synonyms[word]}")' if word in synonyms else f'term = "{word}"' for word in words
            ]
            yield f'{procedure_definition} {{{{ {', '.join(syn_terms)} }}}}'

        if len(words) > 2:
            for i in reversed(range(1, len(words) - 1)):
                word_comps = [
                    f'term = ("{" ".join(word_comp)}")' for word_comp in combinations(words, i + 1)
                ]  # TODO: Add synonyms to this
                yield f'{procedure_definition} {{{{ {", ".join(word_comps)} }}}}'

        yield f'{procedure_definition} {{{{ term = ("{'" "'.join(words)}")}}}}'
        yield f'{procedure_definition} {{{{ term = ("{'" "'.join(words + keywords)}")}}}}'

    def forward(
        self,
        term: str,
        synonyms: dict[str, str],
        keywords: list[str],
    ) -> list[dict]:
        """
        Search SNOMED CT for procedures matching the given term.

        Args:
            term: The search term to query.
            synonyms: A dictionary of synonyms for the words in the search term.
            keywords: A list of keywords to search for.

        Returns:
            list of dictionaries containing procedure details.
        """
        limit = 100
        params = {
            "activeFilter": "true",  # Recommended filter by SNOMED CT
            "termActive": "true",  # Recommended filter by SNOMED CT
            "ecl": f'< 71388002|Procedure| {{{{ term = "{term}"}}}}',
        }
        with httpx.Client(base_url=self.base_url) as client:
            for query in self._build_ecl_queries(term, synonyms, keywords):
                params["ecl"] = query
                response = client.get(f"{self.edition}/concepts", params=params)
                response.raise_for_status()
                items = response.json().get("items", [])

                if items:
                    break

            filtered_matches = [
                {
                    "id": match["conceptId"],
                    # "term": match["pt"]["term"],
                    "fsn": match["fsn"]["term"],
                }
                for match in items
                if match["definitionStatus"] in ["FULLY_DEFINED", "PRIMITIVE"]
            ]
            filtered_matches = sorted(
                filtered_matches,
                key=lambda x: len(x["fsn"]),
            )

            return filtered_matches[:limit]
