from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Any, Type

from smolagents import CodeAgent, Model, MultiStepAgent, Tool, ToolCallingAgent


class Agent(StrEnum):
    CODEAGENT = auto()
    TOOLCALLINGAGENT = auto()
    MULTISTEPAGENT = auto()


@dataclass
class Task:
    prompt: str
    tools: list[Tool] = []
    agent_type: Agent = Agent.TOOLCALLINGAGENT
    agent_params: dict[str, Any] = {}

    @property
    def agent(self) -> Type[MultiStepAgent]:
        match self.agent_type:
            case Agent.CODEAGENT:
                return CodeAgent  # type: ignore[no-any-return]
            case Agent.TOOLCALLINGAGENT:
                return ToolCallingAgent  # type: ignore[no-any-return]
            case Agent.MULTISTEPAGENT:
                return MultiStepAgent  # type: ignore[no-any-return]
            case _:
                return ToolCallingAgent

    def run(self, model: Model, **kwargs: Any) -> Any:
        kwargs = self.agent_params | kwargs
        agent = self.agent(self.tools, model, **kwargs)

        return agent.run(self.prompt)
