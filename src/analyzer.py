"""
Analyzes a chess game with Stockfish to find blunders, mistakes, and inaccuracies.

Usage:
    python3 -m src.analyzer <game_url>
    python3 -m src.analyzer <game_url> --time 0.5
"""

import chess
import chess.pgn
import chess.engine
import json
import io
import argparse
import shutil
from pathlib import Path

DATA_DIR = Path("data/games")
USERNAME = "mattydem"

BLUNDER_CP = 200
MISTAKE_CP = 100
INACCURACY_CP = 50
DEFAULT_TIME = 0.1  # seconds per move


def find_stockfish() -> str:
    path = shutil.which("stockfish")
    if not path:
        raise SystemExit("Stockfish not found. Install with: brew install stockfish")
    return path


def find_game(url: str) -> dict | None:
    url = url.rstrip("/")
    for path in sorted(DATA_DIR.glob("*.json")):
        with open(path) as f:
            games = json.load(f)
        for g in games:
            if g.get("url", "").rstrip("/") == url:
                return g
    return None


def fmt_eval(cp: int) -> str:
    if cp >= 9000:
        return "+M"
    if cp <= -9000:
        return "-M"
    return f"{cp / 100:+.1f}"


def classify(cp_loss: int) -> str | None:
    if cp_loss >= BLUNDER_CP:
        return "blunder"
    if cp_loss >= MISTAKE_CP:
        return "mistake"
    if cp_loss >= INACCURACY_CP:
        return "inaccuracy"
    return None


def analyze(pgn_str: str, username: str, sf_path: str, time_per_move: float) -> None:
    game = chess.pgn.read_game(io.StringIO(pgn_str))
    if not game:
        print("Could not parse PGN.")
        return

    white_name = game.headers.get("White", "?")
    black_name = game.headers.get("Black", "?")
    user_color = chess.WHITE if white_name.lower() == username.lower() else chess.BLACK
    user_side = "White" if user_color == chess.WHITE else "Black"

    print(f"\n{'═' * 54}")
    print(f"  GAME ANALYSIS")
    print(f"{'═' * 54}")
    print(f"  {white_name} (W) vs {black_name} (B)")
    print(f"  You played: {user_side}   |   Result: {game.headers.get('Result', '?')}")
    print(f"  Eval: positive = White is better\n")
    print(f"  Analyzing... ({time_per_move}s per move)\n")

    engine = chess.engine.SimpleEngine.popen_uci(sf_path)

    board = game.board()
    moves = list(game.mainline_moves())

    blunders, mistakes, inaccuracies = [], [], []
    good_moves = 0

    for i, move in enumerate(moves):
        turn = board.turn
        move_num = i // 2 + 1
        is_user = turn == user_color

        if not is_user:
            board.push(move)
            continue

        # Evaluate the position before the user's move (best achievable score)
        info_before = engine.analyse(board, chess.engine.Limit(time=time_per_move))
        s1 = info_before["score"].white().score(mate_score=10000)
        pv = info_before.get("pv", [])
        best_san = board.san(pv[0]) if pv else "?"
        actual_san = board.san(move)

        board.push(move)

        # Evaluate the position after the user's move
        info_after = engine.analyse(board, chess.engine.Limit(time=time_per_move))
        s2 = info_after["score"].white().score(mate_score=10000)

        # cp_loss from the user's perspective (positive = user lost advantage)
        cp_loss = (s1 - s2) if turn == chess.WHITE else (s2 - s1)

        label = classify(cp_loss)
        move_label = (
            f"{move_num}. {actual_san}"
            if user_color == chess.WHITE
            else f"{move_num}... {actual_san}"
        )

        entry = {
            "label": move_label,
            "actual": actual_san,
            "best": best_san,
            "cp_loss": cp_loss,
            "s1": s1,
            "s2": s2,
        }

        if label == "blunder":
            blunders.append(entry)
        elif label == "mistake":
            mistakes.append(entry)
        elif label == "inaccuracy":
            inaccuracies.append(entry)
        else:
            good_moves += 1

    engine.quit()

    # ── Print results ────────────────────────────────────────

    def print_entries(entries: list[dict], symbol: str) -> None:
        for e in entries:
            eval_str = f"[{fmt_eval(e['s1'])} → {fmt_eval(e['s2'])}]"
            best_note = f"   Best: {e['best']}" if e["actual"] != e["best"] else ""
            print(f"  {e['label']}{symbol}   {eval_str}{best_note}")

    sep = "─" * 54

    if blunders:
        print(f"  BLUNDERS ({len(blunders)})")
        print(f"  {sep}")
        print_entries(blunders, "??")
        print()

    if mistakes:
        print(f"  MISTAKES ({len(mistakes)})")
        print(f"  {sep}")
        print_entries(mistakes, "?")
        print()

    if inaccuracies:
        print(f"  INACCURACIES ({len(inaccuracies)})")
        print(f"  {sep}")
        print_entries(inaccuracies, "?!")
        print()

    if not blunders and not mistakes and not inaccuracies:
        print(f"  No blunders, mistakes, or inaccuracies found. Clean game!\n")

    total = len(blunders) + len(mistakes) + len(inaccuracies) + good_moves
    print(f"  {'═' * 52}")
    print(f"  SUMMARY")
    print(f"  {'═' * 52}")
    print(f"  Blunders:      {len(blunders):>3}   (>{BLUNDER_CP / 100:.0f} pawns lost)")
    print(f"  Mistakes:      {len(mistakes):>3}   ({MISTAKE_CP / 100:.0f}–{BLUNDER_CP / 100:.0f} pawns lost)")
    print(f"  Inaccuracies:  {len(inaccuracies):>3}   ({INACCURACY_CP / 100:.1f}–{MISTAKE_CP / 100:.0f} pawns lost)")
    print(f"  Good moves:    {good_moves:>3}")
    print(f"  Total moves:   {total:>3}")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze a chess game with Stockfish")
    parser.add_argument("url", help="chess.com game URL")
    parser.add_argument(
        "--time",
        type=float,
        default=DEFAULT_TIME,
        metavar="SEC",
        help=f"Stockfish analysis time per move in seconds (default: {DEFAULT_TIME})",
    )
    args = parser.parse_args()

    sf_path = find_stockfish()

    game_data = find_game(args.url)
    if not game_data:
        print(f"\nGame not found in local data: {args.url}")
        print("Run python3 -m src.importer to download your games first.")
        return

    pgn = game_data.get("pgn", "")
    if not pgn:
        print("No PGN data found for this game.")
        return

    analyze(pgn, USERNAME, sf_path, args.time)


if __name__ == "__main__":
    main()
