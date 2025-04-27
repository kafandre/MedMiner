from dataclasses import dataclass, field
from typing import Any, Type


@dataclass
class ToolUISetting:
    dependent: str | None = None
    params: dict[str, str] = field(default_factory=dict)


@dataclass
class ToolSetting:
    id: str
    label: str
    type: Type
    ui: ToolUISetting = field(default_factory=ToolUISetting)


class ToolSettingMixin:
    settings: list[ToolSetting] = []

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        for setting in self.settings:
            if (value := kwargs.get(setting.id)) is None:
                raise ValueError(f"Missing required setting: {setting.id}")

            if not isinstance(value, setting.type):
                raise TypeError(f"Expected {setting.type} for setting {setting.id}, got {type(value)}")

            setattr(self, setting.id, value)
