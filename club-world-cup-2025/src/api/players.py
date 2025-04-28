import time

import requests


def get_club_id(club_name: str, retries: int = 3, delay: int = 5) -> int | None:
    """
    Retrieves the club ID from Transfermarkt API based on the club name.

    :param club_name: The name of the club to search for.
    :param retries: The number of retry attempts in case of request failure.
    :param delay: The delay in seconds between retries.
    :return: The club ID if found, otherwise None.
    """
    url = f"https://transfermarkt-api.fly.dev/clubs/search/{club_name}?page_number=1"

    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            results = response.json().get("results", [])

            if results:
                return int(results[0]["id"])

            print(f"Club not found: {club_name}")
            return None

        except requests.exceptions.RequestException as error:
            print(f"Error fetching ID for {club_name}: {error}")
            if attempt < retries - 1:
                time.sleep(delay)

    return None


def get_players(club_id: int) -> list[dict[str, object]]:
    """
    Retrieves the list of players for a given club ID from Transfermarkt API.

    :param club_id: The ID of the club.
    :return: A list of players as dictionaries.
    """
    url = f"https://transfermarkt-api.fly.dev/clubs/{club_id}/players"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json().get("players", [])
    except requests.exceptions.RequestException as error:
        print(f"Error fetching players for club {club_id}: {error}")
        return []
