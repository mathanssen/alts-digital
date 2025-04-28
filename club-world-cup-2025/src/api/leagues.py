import pandas as pd
from api_football_sdk.endpoints.leagues import get_all_leagues


async def find_world_cup_leagues() -> pd.DataFrame:
    """
    Finds leagues related to World Cup or Intercontinental tournaments.

    :return: A pandas DataFrame containing World Cup leagues information.
    """
    leagues = await get_all_leagues()
    world_cups: list[dict[str, str | int]] = []

    for league in leagues:
        league_name = league["league"]["name"].lower()
        if "world cup" in league_name or "intercontinental" in league_name:
            world_cups.append(
                {
                    "league_id": league["league"]["id"],
                    "league_name": league["league"]["name"],
                    "country": league["country"]["name"],
                }
            )

    return pd.DataFrame(world_cups)
