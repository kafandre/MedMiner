import gradio as gr
import pandas as pd

from medminer.pipe import SingleAgentPipeline
from medminer.task.base import TaskRegistry
from medminer.utils.models import DefaultModel


def process_txt_files(
    files: list | None, model_settings: dict[str, str], task_settings: dict[str, str], tasks: list[str]
) -> dict[str, pd.DataFrame]:
    """Process a list of files with the specified tasks.

    Args:
        files: List of file paths to process.
        model_settings: Model settings for the processing.
        task_settings: Task settings for the processing.
        tasks: List of tasks to perform on the files.

    Returns:
        Dictionary containing the processed data.
    """
    if files is None or not tasks:
        return {}

    return {}


def process_csv_file(
    file: str | None,
    column: str | None,
    model_settings: dict[str, str],
    task_settings: dict[str, str],
    tasks: list[str],
) -> dict[str, pd.DataFrame]:
    """Process a CSV file with the specified tasks.

    Args:
        file: Path to the CSV file to process.
        column: Name of the column to process.
        model_settings: Model settings for the processing.
        task_settings: Task settings for the processing.
        tasks: List of tasks to perform on the files.

    Returns:
        Dictionary containing the processed data.
    """
    if file is None or not column or not tasks:
        return {}

    return {}


def process_sql(
    sql: str, model_settings: dict[str, str], task_settings: dict[str, str], tasks: list[str]
) -> dict[str, pd.DataFrame]:
    """Process a SQL query with the specified tasks.

    Args:
        sql: SQL query to process.
        model_settings: Model settings for the processing.
        task_settings: Task settings for the processing.
        tasks: List of tasks to perform on the files.

    Returns:
        Dictionary containing the processed data.
    """
    if not sql or not tasks:
        return {}

    return {}


def process_text(
    request: gr.Request, text: str, model_settings: dict[str, str], task_settings: dict[str, str], tasks: list[str]
) -> dict[str, pd.DataFrame]:
    """Process a text with the specified tasks.

    Args:
        text: Text to process.
        model_settings: Model settings for the processing.
        task_settings: Task settings for the processing.
        tasks: List of tasks to perform on the files.

    Returns:
        Dictionary containing the processed data.
    """
    if not text or not tasks:
        return {}

    reg = TaskRegistry()

    pipe = SingleAgentPipeline(
        tasks=reg.filter(tasks),
        model=DefaultModel(**model_settings).model,
        session_id=request.session_hash,
        **task_settings,
    )

    dfs = pipe.run([text])

    return {task_name.capitalize(): df for task_name, df in dfs.items()}
