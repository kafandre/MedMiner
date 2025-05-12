from abc import ABC, abstractmethod
from pathlib import Path
from textwrap import dedent
from typing import Any, Type, cast
from uuid import uuid4

import pandas as pd
from smolagents import Model, ToolCallingAgent

from medminer.task.base import Task


class Pipeline(ABC):
    """Abstract base class for a pipeline."""

    def __init__(self, tasks: list[Type[Task]], model: Model, **kwargs: Any) -> None:
        """Initialize the pipeline.

        Args:
            tasks: List of tasks to perform.
            model: Model to use for processing.
            kwargs: Dictionary containing both task and model settings.
        """
        if "session_id" not in kwargs:
            kwargs["session_id"] = uuid4().hex
        if "base_dir" not in kwargs:
            kwargs["base_dir"] = Path(__file__).parent.parent / "result"

        self.tasks = [task(model=model, **kwargs) for task in tasks]
        self.model = model
        self.settings = kwargs

    @abstractmethod
    def run(self, data: list[str]) -> dict[str, pd.DataFrame]:
        """Run the pipeline."""
        raise NotImplementedError("Subclasses must implement this method.")


class SingleAgentPipeline(Pipeline):
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

    def build_prompt(self, data: str) -> str:
        """Build the prompt for the agent.

        Args:
            data: Data to process.

        Returns:
            Prompt for the agent.
        """
        prompt = dedent(
            f"""\
        You are a medical data extraction agent.
        You will receive a list of tasks to perform on the data.
        Each task has a name, prompt and a corresponding managed agent.
        Use every the corresponding agent to perfom the task.
        Call the agent with the prompt (enclosed by ```) and the data.
        Provide the information as one text to the agent.
        The agent won't report the result, but will save it to a file.

        Example input:
            Task name: Medication
            Prompt:
            ```
            Instructions ...
            Examples ...
            Column definitions...
            ```

            ---
            Data: ...
        Example Agent instructions:
            Instructions ...
            Examples ...
            Column definitions...
            ---

            Data: ...

        Tasks to perform: {', '.join(task.name for task in self.tasks)}
        """
        )

        task_prompt = f"\n\n{'-' * 80}".join(
            f"Task name: {task.name}\nPrompt: \n```\n{task.prompt}\n```\n\n" for task in self.tasks
        )

        return f"{prompt}{'-' * 80}\n\n{task_prompt}{'-' * 80}\n\nData: \n{data}"

    def run(self, data: list[str]) -> dict[str, pd.DataFrame]:
        """Run the pipeline.

        Args:
            data: Data to process.

        Returns:
            Processed data.
        """
        manager_agent = ToolCallingAgent(tools=[], model=self.model, managed_agents=[task.agent for task in self.tasks])
        for item in data:
            manager_agent.run(
                self.build_prompt(item),
            )

        base_dir: Path = cast(Path, self.settings.get("base_dir"))

        return {
            file_path.stem: pd.read_csv(file_path)
            for file_path in (base_dir / str(self.settings.get("session_id"))).glob("*.csv")
        }
