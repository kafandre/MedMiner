import httpx
from smolagents import tool


@tool
def get_medication_into(
    medication_names: list[str],
) -> dict:
    """
    Get medication information for a given list of medication names.

    Args:
        medication_names: A list of corrected medication names.

    Returns:
        A dictionary containing the medication information (e.g. ATC Code).
    """
    data: dict[str, dict[str, str]] = {}

    base_url = "https://rxnav.nlm.nih.gov/REST/"
    with httpx.Client(base_url=base_url) as client:
        for medication_name in medication_names:
            params = {
                "term": medication_name,
            }
            rxcui = next(
                (
                    cand["rxcui"]
                    for cand in (
                        client.get("approximateTerm.json", params=params)
                        .json()
                        .get("approximateGroup", {})
                        .get("candidate", [])
                    )
                ),
                None,
            )

            if not rxcui:
                data[medication_name] = {}
                continue

            params = {
                "rxcui": rxcui,
            }
            atc = next(
                (
                    cand
                    for cand in (
                        client.get("rxclass/class/byRxcui.json", params=params)
                        .json()
                        .get("rxclassDrugInfoList", {})
                        .get("rxclassDrugInfo", [])
                    )
                    if "atc" in cand["relaSource"].lower()
                ),
                None,
            )

            if not atc:
                data[medication_name] = {}
                continue

            concept = atc.get("rxclassMinConceptItem", {})

            if not concept:
                data[medication_name] = {}
                continue

            data[medication_name] = {
                "atc_id": concept.get("classId"),
                "atc_name": concept.get("className"),
                "atc_type": concept.get("classType"),
            }

    return data
