"""
# Datastore Module

This module provides utilities for managing a local datastore for storing and retrieving data files. 
It includes functionality to set and clear the datastore path, create subdirectories, and handle 
DataFrame storage and retrieval in Parquet format.

Functions:
- set_datastore_path(path): Set the path to the datastore. This must be called before using other functions.
- clear_datastore_path(): Clear the currently set datastore path.
- dump_frame(df, subdir, filename): Save a DataFrame as a Parquet file in the datastore.
- file_exists(subdir, filename): Check if a file exists in the datastore.
- load_frame(subdir, filename): Load a DataFrame from a Parquet file in the datastore.

Make sure to set the datastore path using `set_datastore_path()` before using other functions.
This will cache the path in a local file for future use.
```
"""
import os
import warnings
import pandas as pd


_DATASTORE_PATH_PATH = os.path.join(os.path.dirname(__file__), "_datastore_path.txt")


def set_datastore_path(path: str) -> None:
    """
    Set the path to the datastore file.

    Parameters
    ----------
    path : str
        The path to the datastore file.
    """
    # warn if the path is invalid
    if not os.path.exists(path):
        warnings.warn(
            f'Path "{path}" does not exist. Ensure the path is correct and/or created before proceeding.'
        )

    with open(_DATASTORE_PATH_PATH, "w") as f:
        f.write(path)


def clear_datastore_path() -> None:
    """
    Clear the path to the datastore file.
    """
    with open(_DATASTORE_PATH_PATH, "w") as f:
        f.write("")


def _get_datastore_path() -> str:
    """
    Get the path to the datastore file.
    """
    if os.path.exists(_DATASTORE_PATH_PATH):
        with open(_DATASTORE_PATH_PATH, "r") as f:
            path = f.read().strip()
        return path
    else:
        return None


def _create_subdir(subdir: str) -> None:
    """
    Create a subdirectory in the datastore path.

    Parameters
    ----------
    subdir : str
        The name of the subdirectory to create.
    """
    path = _get_datastore_path()
    if path is None:
        raise ValueError(
            "Datastore path is not set. Please set it using `set_datastore_path()`."
        )

    subdir_path = os.path.join(path, subdir)
    os.makedirs(subdir_path, exist_ok=True)


def dump_frame(df: pd.DataFrame, subdir: str, filename: str) -> None:
    """
    Dump a DataFrame to a Parquet file in the datastore path.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to dump.
    subdir : str
        The name of the subdirectory to create.
    filename : str
        The name of the file to create.
    """
    path = _get_datastore_path()
    if path is None:
        raise ValueError(
            "Datastore path is not set. Please set it using `set_datastore_path()`."
        )

    _create_subdir(subdir)

    file_path = os.path.join(path, subdir, filename)
    df.to_parquet(file_path)


def file_exists(subdir: str, filename: str) -> bool:
    """
    Check if a file exists in the datastore path.

    Parameters
    ----------
    subdir : str
        The name of the subdirectory.
    filename : str
        The name of the file.
    """
    path = _get_datastore_path()
    if path is None:
        raise ValueError(
            "Datastore path is not set. Please set it using `set_datastore_path()`."
        )

    file_path = os.path.join(path, subdir, filename)
    return os.path.exists(file_path)


def load_frame(subdir: str, filename: str) -> pd.DataFrame:
    """
    Load a DataFrame from a Parquet file in the datastore path.

    Parameters
    ----------
    subdir : str
        The name of the subdirectory to create.
    filename : str
        The name of the file to create.

    Returns
    -------
    pd.DataFrame
        The loaded DataFrame.
    """
    path = _get_datastore_path()
    if path is None:
        raise ValueError(
            "Datastore path is not set. Please set it using `set_datastore_path()`."
        )

    file_path = os.path.join(path, subdir, filename)
    return pd.read_parquet(file_path)
