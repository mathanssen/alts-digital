import pandas as pd

from api_football_sdk.endpoints.fixtures import get_fixtures_by_league
from constants import LEAGUES_OF_INTEREST, SEASONS


async def fetch_fixtures_world_cups() -> list[dict[str, object]]:
    """
    Fetches all fixtures for the leagues and seasons of interest.

    :return: A list of fixtures dictionaries.
    """
    all_fixtures: list[dict[str, object]] = []

    for league_id in LEAGUES_OF_INTEREST:
        for season in SEASONS:
            try:
                fixtures = await get_fixtures_by_league(league_id, season)
                if fixtures:
                    all_fixtures.extend(fixtures)
            except Exception as error:
                print(f"Error fetching {league_id} - {season}: {error}")

    return all_fixtures


def flatten_fixtures(fixtures_data: list[dict[str, object]]) -> pd.DataFrame:
    """
    Flattens the raw fixtures data into a structured pandas DataFrame.

    :param fixtures_data: The raw fixtures data.
    :return: A pandas DataFrame containing flattened fixtures.
    """
    fixtures_list: list[dict[str, object]] = []

    for match in fixtures_data:
        fixture = match["fixture"]
        league = match["league"]
        teams = match["teams"]
        goals = match["goals"]
        score = match.get("score", {})

        fixtures_list.append({
            "fixture_id": fixture["id"],
            "date": fixture["date"],
            "venue": fixture.get("venue", {}).get("name"),
            "league_id": league["id"],
            "league_name": league["name"],
            "season": league["season"],
            "round": league.get("round"),
            "home_team_id": teams["home"]["id"],
            "home_team_name": teams["home"]["name"],
            "home_goals": goals["home"],
            "away_team_id": teams["away"]["id"],
            "away_team_name": teams["away"]["name"],
            "away_goals": goals["away"],
            "winner_home": teams["home"]["winner"],
            "winner_away": teams["away"]["winner"],
            "penalty_home": score.get("penalty", {}).get("home"),
            "penalty_away": score.get("penalty", {}).get("away"),
            "status": fixture["status"]["long"],
        })

    return pd.DataFrame(fixtures_list)
