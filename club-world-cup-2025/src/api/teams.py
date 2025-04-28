from api_football_sdk.endpoints.teams import get_team_by_id


async def fetch_team_info(team_id: int) -> dict[str, int | str]:
    """
    Fetches information about a team given its ID.

    :param team_id: The ID of the team.
    :return: A dictionary containing team information.
    """
    response = await get_team_by_id(team_id)
    team = response["team"]

    return {
        "team_id": team_id,
        "team_name": team["name"],
        "country": team["country"],
    }
