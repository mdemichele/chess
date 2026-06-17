"""
Prints a stats summary from locally saved chess.com games.

Usage:
    python3 -m src.stats
    python3 -m src.stats --time-class blitz
    python3 -m src.stats --since 2025-01
"""

import json
import argparse
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone

DATA_DIR = Path("data/games")
USERNAME = "mattydem"


def load_all_games(since: str | None = None, time_class: str | None = None) -> list[dict]:
    games = []
    for path in sorted(DATA_DIR.glob("*.json")):
        month = path.stem
        if since and month < since:
            continue
        with open(path) as f:
            month_games = json.load(f)
        for g in month_games:
            if g.get("rules") != "chess":
                continue
            if time_class and g.get("time_class") != time_class:
                continue
            games.append(g)
    return games


def classify_result(game: dict) -> str:
    """Returns 'win', 'loss', or 'draw' from mattydem's perspective."""
    username = USERNAME.lower()
    white = game["white"]["username"].lower()
    white_result = game["white"]["result"]
    black_result = game["black"]["result"]

    if white == username:
        my_result = white_result
    else:
        my_result = black_result

    if my_result == "win":
        return "win"
    elif my_result in ("agreed", "repetition", "stalemate", "insufficient", "timevsinsufficient", "50move"):
        return "draw"
    else:
        return "loss"


def my_side(game: dict) -> str:
    return "white" if game["white"]["username"].lower() == USERNAME.lower() else "black"


def my_rating(game: dict) -> int | None:
    side = my_side(game)
    return game[side].get("rating")


def opening_name(game: dict) -> str:
    eco_url = game.get("eco", "")
    if not eco_url:
        return "Unknown"
    name = eco_url.rstrip("/").split("/")[-1].replace("-", " ")
    # Trim variation suffixes to keep it to the opening family
    parts = name.split()
    # Cap at 4 words so names stay readable
    return " ".join(parts[:4])


def termination(game: dict) -> str:
    """Extract how the game ended from the PGN headers."""
    pgn = game.get("pgn", "")
    for line in pgn.split("\n"):
        if line.startswith("[Termination "):
            val = line.split('"')[1]
            for keyword in ("checkmate", "resignation", "timeout", "abandoned",
                            "agreement", "repetition", "stalemate", "insufficient"):
                if keyword in val.lower():
                    return keyword
    return "unknown"


def game_end_month(game: dict) -> str:
    ts = game.get("end_time")
    if not ts:
        return "unknown"
    dt = datetime.fromtimestamp(ts, tz=timezone.utc)
    return dt.strftime("%Y-%m")


def record_str(w: int, l: int, d: int) -> str:
    total = w + l + d
    pct = (w + d * 0.5) / total * 100 if total else 0
    return f"{w}W / {l}L / {d}D  ({pct:.1f}% score, {total} games)"


def print_section(title: str) -> None:
    print(f"\n{'─' * 50}")
    print(f"  {title}")
    print(f"{'─' * 50}")


def top_openings(games: list[dict], n: int = 10) -> None:
    stats: dict[str, dict] = defaultdict(lambda: {"win": 0, "loss": 0, "draw": 0})
    for g in games:
        name = opening_name(g)
        result = classify_result(g)
        stats[name][result] += 1

    ranked = sorted(stats.items(), key=lambda x: sum(x[1].values()), reverse=True)[:n]

    print(f"\n  {'Opening':<40} {'Games':>6}  {'Win%':>6}")
    print(f"  {'─'*40}  {'─'*6}  {'─'*6}")
    for name, r in ranked:
        total = r["win"] + r["loss"] + r["draw"]
        win_pct = (r["win"] + r["draw"] * 0.5) / total * 100
        print(f"  {name:<40} {total:>6}  {win_pct:>5.1f}%")


def rating_trend(games: list[dict]) -> None:
    by_month: dict[str, list[int]] = defaultdict(list)
    for g in games:
        month = game_end_month(g)
        r = my_rating(g)
        if r:
            by_month[month].append(r)

    print(f"\n  {'Month':<10}  {'Avg Rating':>12}  {'Peak':>6}  {'Low':>6}  {'Games':>6}")
    print(f"  {'─'*10}  {'─'*12}  {'─'*6}  {'─'*6}  {'─'*6}")
    for month in sorted(by_month):
        ratings = by_month[month]
        print(f"  {month:<10}  {sum(ratings)/len(ratings):>12.0f}  "
              f"{max(ratings):>6}  {min(ratings):>6}  {len(ratings):>6}")


def main():
    parser = argparse.ArgumentParser(description="Chess stats summary for mattydem")
    parser.add_argument("--time-class", choices=["bullet", "blitz", "rapid", "daily"],
                        help="Filter by time control")
    parser.add_argument("--since", metavar="YYYY-MM", help="Only include games from this month onward")
    args = parser.parse_args()

    games = load_all_games(since=args.since, time_class=args.time_class)
    if not games:
        print("No games found. Run python3 -m src.importer first.")
        return

    filter_desc = []
    if args.time_class:
        filter_desc.append(args.time_class)
    if args.since:
        filter_desc.append(f"since {args.since}")
    filter_str = f" ({', '.join(filter_desc)})" if filter_desc else ""

    print(f"\n{'═' * 50}")
    print(f"  CHESS STATS — mattydem{filter_str}")
    print(f"{'═' * 50}")

    # ── Overall record ──────────────────────────────
    print_section("OVERALL RECORD")
    wins = sum(1 for g in games if classify_result(g) == "win")
    losses = sum(1 for g in games if classify_result(g) == "loss")
    draws = sum(1 for g in games if classify_result(g) == "draw")
    print(f"\n  {record_str(wins, losses, draws)}")

    # ── By time control ─────────────────────────────
    print_section("BY TIME CONTROL")
    for tc in ("bullet", "blitz", "rapid", "daily"):
        tc_games = [g for g in games if g.get("time_class") == tc]
        if not tc_games:
            continue
        w = sum(1 for g in tc_games if classify_result(g) == "win")
        l = sum(1 for g in tc_games if classify_result(g) == "loss")
        d = sum(1 for g in tc_games if classify_result(g) == "draw")
        print(f"\n  {tc.capitalize():<8}  {record_str(w, l, d)}")

    # ── By color ────────────────────────────────────
    print_section("BY COLOR")
    for color in ("white", "black"):
        color_games = [g for g in games if my_side(g) == color]
        w = sum(1 for g in color_games if classify_result(g) == "win")
        l = sum(1 for g in color_games if classify_result(g) == "loss")
        d = sum(1 for g in color_games if classify_result(g) == "draw")
        print(f"\n  {color.capitalize():<8}  {record_str(w, l, d)}")

    # ── How games end ───────────────────────────────
    print_section("HOW GAMES END")
    term_counts: dict[str, int] = defaultdict(int)
    for g in games:
        term_counts[termination(g)] += 1
    ranked_terms = sorted(term_counts.items(), key=lambda x: x[1], reverse=True)
    print()
    for term, count in ranked_terms:
        pct = count / len(games) * 100
        print(f"  {term:<20}  {count:>5}  ({pct:.1f}%)")

    # ── Top openings as white ───────────────────────
    print_section("TOP OPENINGS AS WHITE")
    top_openings([g for g in games if my_side(g) == "white"])

    # ── Top openings as black ───────────────────────
    print_section("TOP OPENINGS AS BLACK")
    top_openings([g for g in games if my_side(g) == "black"])

    # ── Rating trend ────────────────────────────────
    print_section("RATING TREND (all time controls combined)")
    rating_trend(games)

    print()


if __name__ == "__main__":
    main()
