import httpx
from smolagents import Tool

from medminer.tools.settings import ToolSetting, ToolSettingMixin


class SNOMEDTool(ToolSettingMixin, Tool):
    """A tool for searching SNOMED CT concepts."""

    name = "search_snomed_procedures"
    description = "Search SNOMED CT for procedures matching the given term."
    inputs = {
        "term": {"type": "string", "description": "The search term to query."},
        "limit": {"type": "integer", "description": "The maximum number of results to return.", "nullable": True},
        "semantic_tag": {"type": "string", "description": "The semantic tag to filter results by.", "nullable": True},
    }
    output_type = "array"
    settings = [
        ToolSetting(id="base_url", label="Base URL", type=str),
        ToolSetting(id="edition", label="Edition", type=str),
    ]
    base_url: str
    edition: str

    def forward(
        self,
        term: str,
        limit: int = 100,
        semantic_tag: str = "procedure",
    ) -> list[dict]:
        """
        Search SNOMED CT for procedures matching the given term.

        Args:
            term (str): The search term to query.
            limit (int): The maximum number of results to return.
            semantic_tag (str): The semantic tag to filter results by.

        Returns:
            list[dict]: A list of dictionaries containing procedure details.
        """

        params = {
            "term": term,
            "activeFilter": "true",  # Recommended filter by SNOMED CT
            "termActive": "true",  # Recommended filter by SNOMED CT
        }
        with httpx.Client(base_url=self.base_url) as client:
            response = client.get(f"{self.edition}/concepts", params=params)
            response.raise_for_status()
            items = response.json().get("items", [])

            filtered_matches = [
                {
                    "id": match["conceptId"],
                    "term": match["pt"]["term"],
                    "fsn": match["fsn"]["term"],
                }
                for match in items
                if match["definitionStatus"] == "FULLY_DEFINED"
                and (semantic_tag is None or semantic_tag in match["fsn"]["term"])
            ]

            return filtered_matches[:limit]
