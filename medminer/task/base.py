from abc import ABC
from dataclasses import dataclass, field
from functools import cache
from textwrap import dedent, indent
from typing import Any, Type, TypeVar

from smolagents import Model, MultiStepAgent, Tool, ToolCallingAgent


@dataclass
class TaskSetting:
    id: str
    label: str
    dependent: str | None = None
    params: dict[str, Any] = field(default_factory=dict)


class Task(ABC):
    name: str
    verbose_name: str
    prompt: str
    agent_type: Type[MultiStepAgent] = ToolCallingAgent
    tools: list[Tool] = []
    agent_params: dict[str, Any] = {}
    settings: list[TaskSetting] = []

    def __init__(
        self,
        model: Model,
        **kwargs: Any,
    ) -> None:
        self._agent = self.agent_type(self.tools, model, **(self.agent_params | kwargs))

    @property
    def agent(self) -> MultiStepAgent:
        return self._agent

    # def get_agent(self, model: Model, **kwargs: Any) -> MultiStepAgent:
    #     return self._agent_type(
    #         self._tools, model,
    #         **(self._agent_params | kwargs)
    #     )

    def run(self, data: str) -> Any:
        return self.agent.run(
            dedent(
                f"""\
                Task name: {self.name}
                Prompt: \n{indent(self.prompt, " " * 4 * 5)}

                {"-" * 80}
                Data: \n{indent(data, " " * 4 * 5)}
                """
            )
        )


T = TypeVar("T", bound=Task)


def register_task(task: Type[T]) -> Type[T]:
    """
    Register a task.
    """
    TaskRegistry().register(task)
    return task


@cache
class TaskRegistry:
    """
    A registry for tasks.
    """

    def __init__(self) -> None:
        self.tasks: dict[str, Type[Task]] = {}

    def register(self, task: Type[Task]) -> Type[Task]:
        """
        Register a task.
        """
        self.tasks[task.name] = task
        return task

    def get(self, name: str) -> Type[Task] | None:
        """
        Get a task by name.
        """
        return self.tasks.get(name)

    def all(self) -> list[Type[Task]]:
        """
        Get all tasks.
        """
        return list(self.tasks.values())

    def all_settings(self) -> list[TaskSetting]:
        """
        Get all task settings.
        """
        return [
            TaskSetting(setting.id, setting.label, task.name, setting.params)
            for task in self.tasks.values()
            for setting in task.settings
        ]
