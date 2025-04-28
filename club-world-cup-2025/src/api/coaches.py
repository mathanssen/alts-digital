from api_football_sdk.endpoints.coachs import get_coach_by_team
from api_football_sdk.endpoints.trophies import get_trophies_by_coach


async def fetch_coach_info(team_id: int) -> dict[str, int | str] | None:
    """
    Fetches the coach information for a given team.

    :param team_id: The ID of the team to fetch the coach for.
    :return: A dictionary containing coach information or None if not found.
    """
    coach = await get_coach_by_team(team_id)
    if not coach:
        return None

    return {
        "coach_id": coach["id"],
        "coach_name": coach["name"],
        "nationality": coach["nationality"],
        "team_id": team_id,
    }


async def fetch_coach_trophies(coach_id: int) -> list[dict[str, str | int]]:
    """
    Fetches the trophies won by a given coach.

    :param coach_id: The ID of the coach to fetch trophies for.
    :return: A list of dictionaries containing trophies information.
    """
    trophies = await get_trophies_by_coach(coach_id)
    return trophies
