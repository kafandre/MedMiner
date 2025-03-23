from dataclasses import dataclass, field
from enum import StrEnum, auto
from textwrap import dedent
from typing import Any, Type

from smolagents import CodeAgent, Model, MultiStepAgent, Tool, ToolCallingAgent


class Agent(StrEnum):
    CODEAGENT = auto()
    TOOLCALLINGAGENT = auto()
    MULTISTEPAGENT = auto()


@dataclass
class Task:
    name: str
    prompt: str
    agent_type: Agent = Agent.TOOLCALLINGAGENT
    tools: list[Tool] = field(default_factory=list)
    agent_params: dict[str, Any] = field(default_factory=dict)

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

    def run(self, model: Model, data: str, **kwargs: Any) -> Any:
        kwargs = self.agent_params | kwargs
        agent = self.agent(self.tools, model, **kwargs)

        return agent.run(
            dedent(
                f"""
                Task name: {self.name}
                Prompt:
                    {self.prompt}

                ---
                {data}
                """
            )
        )
