import asyncio
import json
from pathlib import Path

import pandas as pd
from api.fixtures import fetch_fixtures_world_cups, flatten_fixtures
from api.leagues import find_world_cup_leagues
from processing.enrichment import combine_team_info, enrich_teams


def load_manual_fixtures(manual_folder: str = "data/manual_fixtures/") -> pd.DataFrame:
    """
    Loads manual fixtures from JSON files.

    :param manual_folder: Path to the folder containing fixture JSONs.
    :return: A pandas DataFrame with manual fixtures.
    """
    manual_path = Path(manual_folder)
    manual_files = manual_path.glob("*.json")
    dfs: list[pd.DataFrame] = []

    for file in manual_files:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            dfs.append(pd.DataFrame(data))

    if dfs:
        return pd.concat(dfs, ignore_index=True)

    return pd.DataFrame()


async def process_fixtures() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Fetches API fixtures, combines them with manual fixtures, and enriches team information.

    :return: A tuple with combined fixtures DataFrame and combined teams DataFrame.
    """
    df_leagues = await find_world_cup_leagues()

    fixtures_api = await fetch_fixtures_world_cups()
    df_fixtures_api = flatten_fixtures(fixtures_api)

    df_manual = load_manual_fixtures()

    missing_cols = set(df_fixtures_api.columns) - set(df_manual.columns)
    for col in missing_cols:
        df_manual[col] = None

    df_combined = pd.concat([df_fixtures_api, df_manual], ignore_index=True)

    team_ids = pd.unique(
        pd.concat([df_combined["home_team_id"], df_combined["away_team_id"]])
    )

    teams_api_df = await enrich_teams(
        [int(team_id) for team_id in team_ids if pd.notnull(team_id)]
    )

    teams_manual_path = Path("data/raw/curated/teams_manual.json")
    with open(teams_manual_path, "r", encoding="utf-8") as f:
        manual_teams = json.load(f)

    teams_manual_df = pd.DataFrame(manual_teams)

    teams_combined_df = combine_team_info(teams_api_df, teams_manual_df)

    return df_combined, teams_combined_df
