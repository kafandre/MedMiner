from typing import Any, TypedDict


class FieldConfig(TypedDict):
    params: dict[str, Any]
    id: str


class DependentFieldConfig(FieldConfig):
    dependent: list[str]


class ModelTabConfig(TypedDict):
    name: str
    id: str
    available: bool
    description: str
    fields: list[FieldConfig]


class TaskConfig(TypedDict):
    name: str
    id: str


class TaskSettingConfig(TypedDict):
    description: str
    tasks: list[TaskConfig]
    settings: list[DependentFieldConfig]
