"""
Callback API for Gradio UI.
"""


from enum import IntEnum
from typing import Type

import gradio as gr
import pandas as pd

from medminer.pipe import MultiAgentPipeline, Pipeline, SingleAgentPipeline
from medminer.task.base import TaskRegistry
from medminer.utils.models import DefaultModel


class AgentMode(IntEnum):
    SINGLE = 0
    MULTI = 1


def _process(
    data: list[str], model_settings: dict[str, str], task_settings: dict[str, str], tasks: list[str], agent: str
) -> dict[str, pd.DataFrame]:
    """Process the data with the specified tasks.

    Args:
        data: List of data to process.
        model_settings: Model settings for the processing.
        task_settings: Task settings for the processing.
        tasks: List of tasks to perform on the files.
        agent: Agent mode (single or multi).

    Returns:
        Dictionary containing the processed data.
    """
    if not data or not tasks:
        return {}

    reg = TaskRegistry()

    pipe_cls: Type[Pipeline] = SingleAgentPipeline if agent == AgentMode.SINGLE else MultiAgentPipeline
    pipe = pipe_cls(
        tasks=reg.filter(tasks),
        model=DefaultModel(**model_settings).model,
        **task_settings,
    )

    dfs = pipe.run(data)

    return {task_name.capitalize(): df for task_name, df in dfs.items()}


def process_txt_files(
    request: gr.Request,
    files: list | None,
    model_settings: dict[str, str],
    task_settings: dict[str, str],
    tasks: list[str],
    agent: str,
) -> dict[str, pd.DataFrame]:
    """Process a list of files with the specified tasks.

    Args:
        request: Gradio request object.
        files: List of file paths to process.
        model_settings: Model settings for the processing.
        task_settings: Task settings for the processing.
        tasks: List of tasks to perform on the files.
        agent: Agent mode (single or multi).

    Returns:
        Dictionary containing the processed data.
    """
    if files is None or not tasks:
        return {}

    data: list[str] = []
    for file in files:
        with open(file, "r") as f:
            data.append(f.read())

    return _process(
        data=data,
        model_settings=model_settings,
        task_settings=task_settings | {"session_id": str(request.session_hash)},
        tasks=tasks,
        agent=agent,
    )


def process_csv_file(
    request: gr.Request,
    file: str | None,
    column: str | None,
    model_settings: dict[str, str],
    task_settings: dict[str, str],
    tasks: list[str],
    agent: str,
) -> dict[str, pd.DataFrame]:
    """Process a CSV file with the specified tasks.

    Args:
        request: Gradio request object.
        file: Path to the CSV file to process.
        column: Name of the column to process.
        model_settings: Model settings for the processing.
        task_settings: Task settings for the processing.
        tasks: List of tasks to perform on the files.
        agent: Agent mode (single or multi).

    Returns:
        Dictionary containing the processed data.
    """
    if file is None or not column or not tasks:
        return {}

    df = pd.read_csv(file)
    data: list[str] = df[column].tolist()

    return _process(
        data=data,
        model_settings=model_settings,
        task_settings=task_settings | {"session_id": str(request.session_hash)},
        tasks=tasks,
        agent=agent,
    )


def process_sql(
    request: gr.Request,
    sql: str,
    model_settings: dict[str, str],
    task_settings: dict[str, str],
    tasks: list[str],
    agent: str,
) -> dict[str, pd.DataFrame]:
    """Process a SQL query with the specified tasks.

    Args:
        request: Gradio request object.
        sql: SQL query to process.
        model_settings: Model settings for the processing.
        task_settings: Task settings for the processing.
        tasks: List of tasks to perform on the files.
        agent: Agent mode (single or multi).

    Returns:
        Dictionary containing the processed data.
    """
    if not sql or not tasks:
        return {}

    return {}


def process_text(
    request: gr.Request,
    text: str,
    model_settings: dict[str, str],
    task_settings: dict[str, str],
    tasks: list[str],
    agent: str,
) -> dict[str, pd.DataFrame]:
    """Process a text with the specified tasks.

    Args:
        request: Gradio request object.
        text: Text to process.
        model_settings: Model settings for the processing.
        task_settings: Task settings for the processing.
        tasks: List of tasks to perform on the files.
        agent: Agent mode (single or multi).

    Returns:
        Dictionary containing the processed data.
    """
    if not text or not tasks:
        return {}

    return _process(
        data=[text],
        model_settings=model_settings,
        task_settings=task_settings | {"session_id": str(request.session_hash)},
        tasks=tasks,
        agent=agent,
    )
