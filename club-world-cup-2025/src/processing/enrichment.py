import pandas as pd
from api.teams import fetch_team_info


async def enrich_teams(team_ids: list[int | float]) -> pd.DataFrame:
    """
    Fetches team name and country information from the API.

    :param team_ids: A list of team IDs.
    :return: A pandas DataFrame with enriched team information.
    """
    enriched: list[dict[str, int | str]] = []

    for team_id in team_ids:
        if pd.notnull(team_id):
            try:
                info = await fetch_team_info(int(team_id))
                enriched.append(
                    {
                        "team_id": info["team_id"],
                        "team_name": info["team_name"],
                        "country": info["country"],
                    }
                )
            except Exception as error:
                print(f"Error fetching team_id {team_id}: {error}")

    return pd.DataFrame(enriched)


def combine_team_info(
    teams_api_df: pd.DataFrame,
    teams_manual_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Combines team information from the API and manually defined teams.

    :param teams_api_df: DataFrame with API team data.
    :param teams_manual_df: DataFrame with manually defined team data.
    :return: A combined DataFrame with unique team names.
    """
    teams_api_df["team_name"] = teams_api_df["team_name"].str.strip().str.lower()
    teams_manual_df["team_name"] = teams_manual_df["team_name"].str.strip().str.lower()

    combined = pd.concat([teams_api_df, teams_manual_df], ignore_index=True)
    combined = combined.drop_duplicates(subset="team_name", keep="first")

    return combined.reset_index(drop=True)
