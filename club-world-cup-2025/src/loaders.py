from pathlib import Path

import pandas as pd

from src.utils import safe_read_json


def load_club_titles_data(
    path: str = "data/raw/world_club_titles.json",
) -> pd.DataFrame:
    """
    Loads the club titles data from a JSON file.

    :param path: Path to the JSON file.
    :return: A pandas DataFrame with club titles data.
    """
    data = safe_read_json(path)
    return pd.json_normalize(data, sep="_")


def load_coaches_data(
    path: str = "data/raw/curated/coaches_manual.json",
) -> pd.DataFrame:
    """
    Loads the coaches data from a JSON file.

    :param path: Path to the JSON file.
    :return: A pandas DataFrame with coaches data.
    """
    data = safe_read_json(path)
    return pd.DataFrame(data)


def load_fixtures_data(path: str = "data/raw/curated/fixtures/") -> pd.DataFrame:
    """
    Loads all manual fixtures from JSON files in a directory.

    :param path: Path to the fixtures folder.
    :return: A pandas DataFrame combining all fixture data.
    """
    fixtures_path = Path(path)
    all_fixtures: list[pd.DataFrame] = []

    for file in fixtures_path.glob("*.json"):
        matches = safe_read_json(file)
        all_fixtures.append(pd.DataFrame(matches))

    return pd.concat(all_fixtures, ignore_index=True)
