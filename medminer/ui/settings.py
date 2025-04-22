from typing import Any, TypedDict

from medminer.utils.models import imported_azure_openai, impoted_hf_transformer


class ModelTabFieldConfig(TypedDict):
    params: dict[str, Any]
    id: str


class ModelTabConfig(TypedDict):
    name: str
    id: str
    available: bool
    description: str
    fields: list[ModelTabFieldConfig]


MODEL_TABS: list[ModelTabConfig] = [
    {
        "name": "HF Transformer",
        "id": "hf_transformer",
        "available": impoted_hf_transformer,
        "description": "Enter a Model name of a HuggingFace transformer.",
        "fields": [
            {"params": {"label": "Model name", "placeholder": "Qwen/Qwen2.5-Coder-32B-Instruct"}, "id": "hf_model_id"},
        ],
    },
    {
        "name": "Azure OpenAI",
        "id": "azure_openai",
        "available": imported_azure_openai,
        "description": "Enter the model name, endpoint, and API key.",
        "fields": [
            {"params": {"label": "Model name", "placeholder": "gpt-4.1"}, "id": "oai_model_id"},
            {
                "params": {"label": "Endpoint", "placeholder": "https://<your-resource-name>.openai.azure.com/"},
                "id": "oai_azure_endpoint",
            },
            {"params": {"label": "API Version", "placeholder": "2024-12-01-preview"}, "id": "oai_api_version"},
            {"params": {"label": "API Key", "placeholder": "<api-key>", "type": "password"}, "id": "oai_api_key"},
        ],
    },
]
