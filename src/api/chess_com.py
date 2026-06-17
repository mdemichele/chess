import requests
import time

BASE_URL = "https://api.chess.com/pub"
HEADERS = {"User-Agent": "chess-improvement-tool/1.0 (github.com/mdemichele/chess)"}


def _get(url: str) -> dict:
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()


def get_player_stats(username: str) -> dict:
    return _get(f"{BASE_URL}/player/{username}/stats")


def get_game_archives(username: str) -> list[str]:
    data = _get(f"{BASE_URL}/player/{username}/games/archives")
    return data.get("archives", [])


def get_games_for_month(archive_url: str, delay: float = 0.5) -> list[dict]:
    """Fetch all games from an archive URL. Delay between requests to respect rate limits."""
    time.sleep(delay)
    data = _get(archive_url)
    return data.get("games", [])
