import time

import pandas as pd
from api.players import get_club_id, get_players
from constants import CONTINENT_MAPPING, COUNTRY_MAPPING, TEAM_MAPPING


def fetch_players_data() -> pd.DataFrame:
    """
    Fetches players' data from clubs participating in the World Cup.

    :return: A pandas DataFrame with players, clubs, countries, continents, and market values.
    """
    clubs = list(TEAM_MAPPING.keys())
    players: list[dict[str, int | str | float | None]] = []

    for club in clubs:
        club_id = get_club_id(club)
        if club_id:
            players_list = get_players(club_id)
            for player in players_list:
                players.append(
                    {
                        "player_id": int(player["id"]),
                        "name": player["name"],
                        "nationality": (
                            player["nationality"][0]
                            if player.get("nationality")
                            else None
                        ),
                        "club": club,
                        "position": player.get("position"),
                        "age": player.get("age"),
                        "market_value_eur": player.get("marketValue"),
                    }
                )
            time.sleep(1)
        else:
            print(f"Club ID not found for: {club}")

    players_df = pd.DataFrame(players)
    players_df["club"] = players_df["club"].replace(TEAM_MAPPING)
    players_df["country"] = players_df["nationality"].replace(COUNTRY_MAPPING)
    players_df["continent"] = players_df["country"].replace(CONTINENT_MAPPING)

    return players_df


def summarize_players_by_club(players_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generates a summary of players by club.

    :param players_df: A pandas DataFrame containing player data.
    :return: A pandas DataFrame with number of players and total market value by club.
    """
    return (
        players_df.groupby("club")
        .agg(
            num_players=("player_id", "count"),
            total_market_value_eur=("market_value_eur", "sum"),
        )
        .sort_values(by="total_market_value_eur", ascending=False)
        .reset_index()
    )
