from abc import ABC
from functools import cache
from textwrap import dedent, indent
from typing import Any, Type, TypeVar, cast
from uuid import uuid4

from smolagents import Model, MultiStepAgent, Tool, ToolCallingAgent

from medminer.tools.settings import ToolSetting, ToolSettingMixin


class Task(ABC):
    name: str
    verbose_name: str
    prompt: str
    agent_type: Type[MultiStepAgent] = ToolCallingAgent
    tools: list[Tool | Type[Tool]] = []
    agent_params: dict[str, Any] = {}

    def __init__(
        self,
        model: Model,
        **kwargs: Any,
    ) -> None:
        kwargs["task_name"] = self.name
        if "session_id" not in kwargs:
            kwargs["session_id"] = uuid4().hex

        tools = []
        for tool in self.tools:
            if not isinstance(tool, type):
                tools.append(tool)
                continue

            if not issubclass(tool, ToolSettingMixin):
                continue

            tools.append(tool(**kwargs))

        self._agent = self.agent_type(tools, model, **self.agent_params)

    @property
    def agent(self) -> MultiStepAgent:
        return self._agent

    @classmethod
    def settings(cls) -> list[ToolSetting]:
        """
        Get the settings for the task.
        """
        settings: dict[str, ToolSetting] = {}
        for tool in cls.tools:
            if not isinstance(tool, type):
                continue

            if not issubclass(tool, ToolSettingMixin):
                continue

            for setting in tool.settings:
                if setting.id in settings:
                    continue

                settings[setting.id] = setting

        return list(settings.values())

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

    def all_settings(self) -> list[ToolSetting]:
        """
        Get all task settings.
        """
        settings: dict[str, ToolSetting] = {}
        for task in self.tasks.values():
            for setting in task.settings():
                if setting.id in settings:
                    cast(dict, settings[setting.id]).setdefault("ui", {}).setdefault("dependent", []).append(setting.id)
                    continue

                settings[setting.id] = setting

        return list(settings.values())
