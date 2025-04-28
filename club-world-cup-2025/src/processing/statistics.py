from collections import defaultdict

import pandas as pd


def generate_club_statistics(
    fixtures_df: pd.DataFrame,
    teams_info_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Generates consolidated club statistics from fixtures.

    :param fixtures_df: Combined fixtures DataFrame.
    :param teams_info_df: Combined teams information DataFrame.
    :return: A pandas DataFrame with club statistics.
    """
    club_stats: dict[str, dict[str, object]] = defaultdict(
        lambda: {
            "club_name": "",
            "country": "",
            "continent": "",
            "editions_played": set(),
            "matches_played": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "goals_for": 0,
            "goals_against": 0,
            "titles": 0,
            "runners_up": 0,
        }
    )

    teams_info_df["team_name_norm"] = teams_info_df["team_name"].str.lower().str.strip()
    teams_info_lookup = teams_info_df.set_index("team_name_norm").to_dict(orient="index")

    for _, row in fixtures_df.iterrows():
        home = row["home_team_name"].strip().lower()
        away = row["away_team_name"].strip().lower()

        season = row["season"]
        home_goals = row["home_goals"]
        away_goals = row["away_goals"]

        for team_name, goals_for, goals_against, winner in [
            (home, home_goals, away_goals, row["winner_home"]),
            (away, away_goals, home_goals, row["winner_away"]),
        ]:
            if team_name not in club_stats:
                team_info = teams_info_lookup.get(team_name, {})
                club_stats[team_name].update({
                    "club_name": team_info.get("team_name", team_name.title()),
                    "country": team_info.get("country", "Unknown"),
                    "continent": team_info.get("continent", "Unknown"),
                })

            stats = club_stats[team_name]
            stats["matches_played"] += 1
            stats["goals_for"] += goals_for or 0
            stats["goals_against"] += goals_against or 0
            stats["editions_played"].add(season)

            if winner is True:
                stats["wins"] += 1
            elif winner is False:
                stats["losses"] += 1
            else:
                stats["draws"] += 1

        if isinstance(row["round"], str) and row["round"].lower() == "final":
            if row["winner_home"] is True:
                club_stats[home]["titles"] += 1
                club_stats[away]["runners_up"] += 1
            elif row["winner_away"] is True:
                club_stats[away]["titles"] += 1
                club_stats[home]["runners_up"] += 1

    stats_list = [
        {
            "club_name": stats["club_name"],
            "country": stats["country"],
            "continent": stats["continent"],
            "editions_played": len(stats["editions_played"]),
            "matches_played": stats["matches_played"],
            "wins": stats["wins"],
            "draws": stats["draws"],
            "losses": stats["losses"],
            "goals_for": stats["goals_for"],
            "goals_against": stats["goals_against"],
            "titles": stats["titles"],
            "runners_up": stats["runners_up"],
        }
        for stats in club_stats.values()
    ]

    return pd.DataFrame(stats_list)
