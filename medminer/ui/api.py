import pandas as pd


def process_docs(docs: list[str], tasks: list[str]) -> pd.DataFrame:
    """
    Process a list of documents with the specified tasks.

    Parameters
    ----------
    docs : list[str]
        List of documents to process.
    tasks : list[str]
        List of tasks to perform on the documents.

    Returns
    -------
    list[str]
        List of processed documents.
    """
    results = []
    for doc in docs:
        results.append(doc)

    return pd.DataFrame(data={"text": docs})


def process_files(files: list | None, tasks: list[str]) -> pd.DataFrame:
    """
    Process a list of files with the specified tasks.

    Parameters
    ----------
    files : list
        List of file paths to process.
    tasks : list[str]
        List of tasks to perform on the files.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the processed text.
    """
    if files is None or not tasks:
        return pd.DataFrame()

    docs = []

    for file_name in files:
        with open(file_name, "r") as file:
            docs.append(file.read())

    return process_docs(docs, tasks)


def process_sql(sql: str, tasks: list[str]) -> pd.DataFrame:
    """
    Process a SQL query with the specified tasks.

    Parameters
    ----------
    sql : str
        SQL query to process.
    tasks : list[str]
        List of tasks to perform on the SQL query.
    """
    return pd.DataFrame()


def process_text(text: str, tasks: list[str]) -> pd.DataFrame:
    """
    Process a text with the specified tasks.

    Parameters
    ----------
    text : str
        Text to process.
    tasks : list[str]
        List of tasks to perform on the text.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the processed text.
    """
    return process_docs([text], tasks)
