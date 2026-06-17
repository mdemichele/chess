"""
Analyzes move-by-move win rates for a given opening to find where games go wrong.

Usage:
    python3 -m src.opening_analysis "Bishops Opening Berlin Defense"
    python3 -m src.opening_analysis "Italian Game"
    python3 -m src.opening_analysis "Italian Game" --color white
    python3 -m src.opening_analysis "Italian Game" --depth 8
"""

import json
import re
import argparse
from pathlib import Path
from collections import defaultdict

DATA_DIR = Path("data/games")
USERNAME = "mattydem"


def load_all_games() -> list[dict]:
    games = []
    for path in sorted(DATA_DIR.glob("*.json")):
        with open(path) as f:
            games += json.load(f)
    return [g for g in games if g.get("rules") == "chess"]


def classify_result(game: dict) -> str:
    username = USERNAME.lower()
    side = "white" if game["white"]["username"].lower() == username else "black"
    result = game[side]["result"]
    if result == "win":
        return "win"
    elif result in ("agreed", "repetition", "stalemate", "insufficient", "timevsinsufficient", "50move"):
        return "draw"
    else:
        return "loss"


def my_side(game: dict) -> str:
    return "white" if game["white"]["username"].lower() == USERNAME.lower() else "black"


def parse_moves(pgn: str) -> list[str]:
    # Strip headers
    pgn = re.sub(r'\[[^\]]*\]', '', pgn)
    # Strip clock and eval annotations
    pgn = re.sub(r'\{[^}]*\}', '', pgn)
    # Strip move numbers (e.g. "1." "1...")
    pgn = re.sub(r'\d+\.+', '', pgn)
    # Strip result
    pgn = re.sub(r'(1-0|0-1|1/2-1/2|\*)', '', pgn)
    return pgn.split()


def build_tree(games: list[dict], max_depth: int) -> dict:
    """
    Returns a nested dict tree:
      node = { "win": int, "loss": int, "draw": int, "children": { move: node } }
    """
    root: dict = {"win": 0, "loss": 0, "draw": 0, "children": {}}

    for game in games:
        moves = parse_moves(game.get("pgn", ""))
        result = classify_result(game)
        node = root
        node[result] += 1
        for move in moves[:max_depth]:
            if move not in node["children"]:
                node["children"][move] = {"win": 0, "loss": 0, "draw": 0, "children": {}}
            node = node["children"][move]
            node[result] += 1

    return root


def score_pct(node: dict) -> float:
    total = node["win"] + node["loss"] + node["draw"]
    if total == 0:
        return 0.0
    return (node["win"] + node["draw"] * 0.5) / total * 100


def total_games(node: dict) -> int:
    return node["win"] + node["loss"] + node["draw"]


def print_tree(node: dict, depth: int, max_depth: int, min_games: int,
               move_num: int, is_my_turn: bool, prefix: str = "", label: str = "") -> None:
    if depth > max_depth:
        return

    games = total_games(node)
    pct = score_pct(node)
    bar = score_bar(pct)

    if label:
        mover = "You" if is_my_turn else "Opp"
        print(f"{prefix}{label}  [{mover}]  {games} games  {pct:.0f}%  {bar}")

    children = node["children"]
    # Sort by game count descending
    ranked = sorted(children.items(), key=lambda x: total_games(x[1]), reverse=True)
    # Only show moves with enough games
    ranked = [(m, n) for m, n in ranked if total_games(n) >= min_games]

    for i, (move, child) in enumerate(ranked):
        is_last = i == len(ranked) - 1
        connector = "└─ " if is_last else "├─ "
        extension = "   " if is_last else "│  "
        next_move_num = move_num + (1 if not is_my_turn else 0)
        move_label = f"{move_num}." + move if is_my_turn else move
        print_tree(child, depth + 1, max_depth, min_games,
                   next_move_num, not is_my_turn,
                   prefix + extension, connector + move_label)


def score_bar(pct: float) -> str:
    filled = round(pct / 10)
    return f"[{'█' * filled}{'░' * (10 - filled)}]"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("opening", help='Opening name, e.g. "Italian Game"')
    parser.add_argument("--color", choices=["white", "black"], help="Filter to one color")
    parser.add_argument("--depth", type=int, default=10, help="Max ply depth to show (default 10)")
    parser.add_argument("--min-games", type=int, default=5, help="Min games to show a branch (default 5)")
    args = parser.parse_args()

    all_games = load_all_games()

    # Match by ECO URL (case-insensitive, spaces→hyphens)
    pattern = args.opening.replace(" ", "-").lower()
    matched = [g for g in all_games if pattern in g.get("eco", "").lower()]

    if args.color:
        matched = [g for g in matched if my_side(g) == args.color]

    if not matched:
        print(f"No games found for '{args.opening}'" +
              (f" as {args.color}" if args.color else ""))
        return

    wins = sum(1 for g in matched if classify_result(g) == "win")
    losses = sum(1 for g in matched if classify_result(g) == "loss")
    draws = sum(1 for g in matched if classify_result(g) == "draw")
    total = len(matched)
    pct = (wins + draws * 0.5) / total * 100

    color_str = f" as {args.color}" if args.color else ""
    print(f"\n{'═' * 60}")
    print(f"  {args.opening.upper()}{color_str.upper()}")
    print(f"  {wins}W / {losses}L / {draws}D  ({pct:.1f}% score, {total} games)")
    print(f"{'═' * 60}")

    # Determine whose turn it is on move 1
    # If you play white, you move first (is_my_turn=True on ply 1)
    # If you play black, opponent moves first (is_my_turn=False on ply 1)
    if args.color == "black":
        starts_as_mine = False
    elif args.color == "white":
        starts_as_mine = True
    else:
        # Mixed — label based on majority color
        white_count = sum(1 for g in matched if my_side(g) == "white")
        starts_as_mine = white_count > total / 2

    print(f"\n  Move tree (min {args.min_games} games per branch):\n")
    tree = build_tree(matched, args.depth)
    print_tree(tree, 0, args.depth, args.min_games,
               move_num=1, is_my_turn=starts_as_mine)
    print()


if __name__ == "__main__":
    main()
