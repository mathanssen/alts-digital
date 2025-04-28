import json
from pathlib import Path

import pandas as pd


def standardize_names(
    df: pd.DataFrame,
    columns: list[str],
    mapping: dict[str, str],
) -> pd.DataFrame:
    """
    Applies a name mapping to multiple columns in a DataFrame.

    :param df: Input DataFrame.
    :param columns: List of columns to standardize.
    :param mapping: Dictionary with name mappings.
    :return: DataFrame with standardized names.
    """
    df_copy = df.copy()

    for column in columns:
        if column in df_copy.columns:
            df_copy[column] = df_copy[column].str.lower().str.strip().replace(mapping)

    return df_copy


def safe_read_json(path: str | Path) -> dict | list:
    """
    Safely reads a JSON file with UTF-8 encoding.

    :param path: Path to the JSON file.
    :return: Loaded JSON content as dict or list.
    """
    file_path = Path(path)

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def safe_to_excel(df: pd.DataFrame, path: str | Path) -> None:
    """
    Safely saves a DataFrame to an Excel file at the specified path.

    :param df: DataFrame to save.
    :param path: Destination path for the Excel file.
    """
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(file_path, index=False)
