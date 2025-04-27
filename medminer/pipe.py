from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Type, cast
from uuid import uuid4

import pandas as pd
from smolagents import Model

from medminer.task.base import Task


class Pipeline(ABC):
    """Abstract base class for a pipeline."""

    def __init__(self, tasks: list[Type[Task]], model: Model, **kwargs: Any) -> None:
        """Initialize the pipeline.

        Args:
            tasks: List of tasks to perform.
            model: Model to use for processing.
            settings: Dictionary containing both task and model settings.
        """
        if "session_id" not in kwargs:
            kwargs["session_id"] = uuid4().hex
        if "base_dir" not in kwargs:
            kwargs["base_dir"] = Path(__file__).parent.parent / "result"

        self.tasks = [task(model=model, **kwargs) for task in tasks]
        self.model = model
        self.settings = kwargs

    @abstractmethod
    def run(self, *args: Any, **kwargs: Any) -> dict[str, pd.DataFrame]:
        """Run the pipeline."""
        pass


class TaskPipeline(Pipeline):
    """Pipeline for running tasks."""

    def run(self, data: list[str]) -> dict[str, pd.DataFrame]:
        """Run the pipeline.

        Args:
            data: Data to process.

        Returns:
            Processed data.
        """
        for task in self.tasks:
            for item in data:
                task.run(item)

        base_dir: Path = cast(Path, self.settings.get("base_dir"))

        return {
            task.name: pd.read_csv(file_path)
            for file_path in (base_dir / str(self.settings.get("session_id"))).glob("*.csv")
        }


class MultiAgentPipeline(Pipeline):
    """Pipeline for running multiple agents."""

    def run(self, data: str) -> dict[str, pd.DataFrame]:
        """Run the pipeline.

        Args:
            data: Data to process.

        Returns:
            Processed data.
        """
        return {}
