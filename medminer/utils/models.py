import os

from smolagents import Model

try:
    import torch  # noqa: F401
    from smolagents import TransformersModel
    from transformers import (
        AutoModelForCausalLM,  # noqa: F401
        AutoModelForImageTextToText,  # noqa: F401
        AutoProcessor,  # noqa: F401
        AutoTokenizer,  # noqa: F401
    )

    impoted_hf_transformer = True
except ImportError:
    impoted_hf_transformer = False

try:
    import openai  # noqa: F401
    from smolagents import AzureOpenAIServerModel

    imported_azure_openai = True
except ImportError:
    imported_azure_openai = False


class DefaultModel:
    def __init__(self, **kwargs: str) -> None:
        self._model = None

        if imported_azure_openai:
            self._model = AzureOpenAIServerModel(
                model_id=kwargs.get("model_id", "") or os.getenv("AZURE_OPENAI_MODEL", ""),
                azure_endpoint=kwargs.get("azure_endpoint", "") or os.getenv("AZURE_OPENAI_ENDPOINT", ""),
                api_key=kwargs.get("api_key", "") or os.getenv("AZURE_OPENAI_API_KEY", ""),
                api_version=kwargs.get("api_version", "") or os.getenv("OPENAI_API_VERSION", ""),
            )

        if impoted_hf_transformer:
            self._model = TransformersModel(
                model_id=kwargs.get("model_id", "") or os.getenv("HF_MODEL", ""),
            )

    @property
    def model(self) -> Model:
        if self._model is None:
            raise ValueError("")
        return self._model
