"""
Imports games from chess.com and saves them locally as JSON.

Usage:
    python -m src.importer                  # import all games
    python -m src.importer --since 2025-01  # import from a specific month onward
    python -m src.importer --month 2025-06  # import a single month
"""

import json
import argparse
from pathlib import Path
from src.api.chess_com import get_game_archives, get_games_for_month

USERNAME = "mattydem"
DATA_DIR = Path("data/games")


def archive_url_to_month(url: str) -> str:
    parts = url.rstrip("/").split("/")
    return f"{parts[-2]}-{parts[-1]}"


def month_to_path(month: str) -> Path:
    return DATA_DIR / f"{month}.json"


def load_existing(month: str) -> list[dict]:
    path = month_to_path(month)
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return []


def save_games(month: str, games: list[dict]) -> None:
    path = month_to_path(month)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(games, f, indent=2)


def import_month(archive_url: str, force: bool = False) -> int:
    month = archive_url_to_month(archive_url)
    path = month_to_path(month)

    if path.exists() and not force:
        existing = load_existing(month)
        print(f"  {month}: skipped ({len(existing)} games already saved)")
        return 0

    games = get_games_for_month(archive_url)
    save_games(month, games)
    print(f"  {month}: saved {len(games)} games")
    return len(games)


def import_all(since: str | None = None, only_month: str | None = None, force: bool = False) -> None:
    print(f"Fetching game archives for {USERNAME}...")
    archives = get_game_archives(USERNAME)

    if only_month:
        archives = [a for a in archives if archive_url_to_month(a) == only_month]
        if not archives:
            print(f"No archive found for {only_month}")
            return

    if since:
        archives = [a for a in archives if archive_url_to_month(a) >= since]

    print(f"Found {len(archives)} month(s) to process.\n")
    total = 0
    for url in archives:
        total += import_month(url, force=force)

    print(f"\nDone. {total} new games imported.")


def main():
    parser = argparse.ArgumentParser(description="Import chess.com games for mattydem")
    parser.add_argument("--since", metavar="YYYY-MM", help="Import games from this month onward")
    parser.add_argument("--month", metavar="YYYY-MM", help="Import only this specific month")
    parser.add_argument("--force", action="store_true", help="Re-download even if already saved")
    args = parser.parse_args()

    import_all(since=args.since, only_month=args.month, force=args.force)


if __name__ == "__main__":
    main()
