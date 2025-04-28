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
    """Default model class.
    This class is used to initialize the model based on the provided parameters.
    It checks for the presence of either Hugging Face Transformers or Azure OpenAI models.
    If neither is available, it raises a ValueError.
    """

    def __init__(self, **kwargs: str) -> None:
        """Initialize the model.

        Args:
            kwargs: Keyword arguments containing model parameters.
        """
        self._model = None

        if impoted_hf_transformer and (model_id := kwargs.get("hf_model_id", "") or os.getenv("HF_MODEL", "")):
            self._model = TransformersModel(
                model_id=model_id,
            )
        elif (
            imported_azure_openai
            and (model_id := kwargs.get("oai_model_id", "") or os.getenv("AZURE_OPENAI_MODEL", ""))
            and (azure_endpoint := kwargs.get("oai_azure_endpoint", "") or os.getenv("AZURE_OPENAI_ENDPOINT", ""))
            and (api_key := kwargs.get("oai_api_key", "") or os.getenv("AZURE_OPENAI_API_KEY", ""))
            and (api_version := kwargs.get("oai_api_version", "") or os.getenv("OPENAI_API_VERSION", ""))
        ):
            self._model = AzureOpenAIServerModel(
                model_id=model_id,
                azure_endpoint=azure_endpoint,
                api_key=api_key,
                api_version=api_version,
            )

    @property
    def model(self) -> Model:
        """Get the model.

        Returns:
            Model: The initialized model.
        Raises:
            ValueError: If the model is not initialized.
        """
        if self._model is None:
            raise ValueError("")
        return self._model
