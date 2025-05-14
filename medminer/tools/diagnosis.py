"""
This module contains various tools for extracting and processing medical data.
"""

import time
from typing import Any

import httpx
from smolagents import Tool, tool

from medminer.tools.settings import ToolSetting, ToolSettingMixin, ToolUISetting


@tool
def extract_diagnosis_data(
    data: list[dict],
) -> list[dict]:
    """
    Adds extracted data to the task memory.

    Example:
        >>> data = [
        ...     {"patient_id": 1, "diagnosis": "Myocardial Infarction"},
        ...     {"patient_id": 2, "diagnosis": "colon cancer"},
        ... ]
        >>> extract_diagnosis_data("diagnosis", data)

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
    """
    return data


class ICDDiagnosisTool(ToolSettingMixin, Tool):
    """A tool for looking up ICD-11 codes for a list of terms."""

    name = "lookup_icd11"
    description = "Lookup ICD-11 codes for a list of terms."
    inputs = {
        "terms": {
            "type": "array",
            "items": {"type": "string"},
            "description": "A list of terms to search for in the ICD-11 database.",
        },
    }
    output_type = "array"

    settings = [
        ToolSetting(id="icd_client_id", label="ICD Client ID", type=str),
        ToolSetting(
            id="icd_client_secret", label="ICD Client Secret", type=str, ui=ToolUISetting(params={"type": "password"})
        ),
    ]
    icd_client_id: str
    icd_client_secret: str

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self._token_cache = {"token": None, "expires_at": 0}

    def get_token(self) -> str:
        """
        Authenticate with the WHO ICD API and return an access token.
        Caches the token for the period it is valid to reduce roundtrip time.
        """
        # Check if the cached token is still valid
        if self._token_cache["token"] and time.time() < self._token_cache["expires_at"]:  # type: ignore[operator]
            return self._token_cache["token"]  # type: ignore[return-value]

        payload = {
            "client_id": self.icd_client_id,
            "client_secret": self.icd_client_secret,
            "scope": "icdapi_access",
            "grant_type": "client_credentials",
        }
        base_url = "https://icdaccessmanagement.who.int/"
        with httpx.Client(verify=True, base_url=base_url) as client:
            response = client.post("connect/token", data=payload)
            response.raise_for_status()
            response_data = response.json()
            token = response_data.get("access_token")
            expires_in = response_data.get("expires_in", 3600)  # Default to 1 hour if not provided

            # Cache the token and its expiry time
            self._token_cache["token"] = token
            self._token_cache["expires_at"] = time.time() + expires_in

            return token  # type: ignore[no-any-return]

    def forward(self, terms: list[str]) -> list[dict]:
        """
        Lookup ICD-11 codes for a list of terms.

        Args:
            terms: A list of terms to search for in the ICD-11 database.

        Returns:
            A list of dictionaries containing the ICD-11 codes and their title and scores.

        Example:
            >>> terms = ["Myocardial Infarction", "colon cancer"]
            >>> lookup_icd11(terms)
        """
        token = self.get_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Accept-Language": "en",
            "API-Version": "v2",
        }
        base_url = "https://id.who.int/"
        with httpx.Client(verify=True, base_url=base_url) as client:
            results = []
            for term in terms:
                params = {"q": term, "useFlexisearch": "true"}

                response = client.get("icd/release/11/2022-02/mms/search", headers=headers, params=params)
                try:
                    response.raise_for_status()
                except httpx.HTTPStatusError as e:
                    print("💥 Token request failed:")
                    print("Status:", e.response.status_code)
                    print("Response:", e.response.text)
                    raise
                data = response.json()
                candidates = [
                    {
                        "code": candidate.get("theCode"),
                        "score": candidate.get("score"),
                        "title": candidate.get("title"),
                    }
                    for candidate in data.get("destinationEntities", [])
                ]
                # filter for score  > 0.3 # TODO: maybe make this a parameter
                candidates = [c for c in candidates if c["score"] > 0.3]
                # sort by score descending
                candidates.sort(key=lambda x: x["score"], reverse=True)

                results.append(
                    {
                        "term": term,
                        "candidates": candidates,
                    }
                )

        return results
