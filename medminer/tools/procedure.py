import httpx


def search_snomed_procedures(term: str, limit: int = 100, semantic_tag: str = "procedure") -> list[dict]:
    """
    Search SNOMED CT for procedures matching the given term using a Snowstorm server.

    Args:
        term (str): The search term to query.
        limit (int): The maximum number of results to return.
        semantic_tag (str): The semantic tag to filter results by.

    Returns:
        list[dict]: A list of dictionaries containing procedure details.
    """
    base_url = "http://localhost:8080"  # Replace with your Snowstorm server URL
    edition = "MAIN"  # Replace with the appropriate edition if needed

    url = f"{base_url}/{edition}/concepts"

    params = {
        "term": term,
        "activeFilter": "true",  # Recommended filter by SNOMED CT
        "termActive": "true",  # Recommended filter by SNOMED CT
    }

    with httpx.Client() as client:
        response = client.get(url, params=params)
        response.raise_for_status()
        items = response.json().get("items", [])

        filtered_matches = [
            {
                "id": match["conceptId"],
                "term": match["pt"]["term"],
                "fsn": match["fsn"]["term"],
            }
            for match in items
            if match["definitionStatus"] == "FULLY_DEFINED" and (semantic_tag is None or semantic_tag in match["fsn"]["term"])
        ]

        return filtered_matches[:limit]
