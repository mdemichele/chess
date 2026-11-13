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


def analyze_game(pgn_str: str, username: str, sf_path: str, time_per_move: float) -> dict | None:
    """
    Evaluates every position in the game once and returns structured results.

    Each entry in "moves" covers one ply. Evals are centipawns from White's
    perspective; "s1"/"s2" are the evals before/after the move.
    """
    game = chess.pgn.read_game(io.StringIO(pgn_str))
    if not game:
        return None

    white_name = game.headers.get("White", "?")
    black_name = game.headers.get("Black", "?")
    user_color = chess.WHITE if white_name.lower() == username.lower() else chess.BLACK

    engine = chess.engine.SimpleEngine.popen_uci(sf_path)
    board = game.board()
    moves = list(game.mainline_moves())

    def evaluate() -> tuple[int, chess.Move | None]:
        if board.is_game_over():
            outcome = board.outcome()
            if outcome.winner is None:
                return 0, None
            return (10000 if outcome.winner == chess.WHITE else -10000), None
        info = engine.analyse(board, chess.engine.Limit(time=time_per_move))
        pv = info.get("pv", [])
        return info["score"].white().score(mate_score=10000), (pv[0] if pv else None)

    try:
        start_fen = board.fen()
        evals = []
        # Each position is evaluated once: the eval after a move is the eval before the next
        s1, best = evaluate()
        for i, move in enumerate(moves):
            turn = board.turn
            best_san = board.san(best) if best else "?"
            best_uci = best.uci() if best else None
            actual_san = board.san(move)
            board.push(move)
            s2, next_best = evaluate()

            # cp_loss from the mover's perspective (positive = mover lost advantage)
            cp_loss = (s1 - s2) if turn == chess.WHITE else (s2 - s1)
            move_num = i // 2 + 1
            evals.append({
                "ply": i + 1,
                "label": f"{move_num}. {actual_san}" if turn == chess.WHITE else f"{move_num}... {actual_san}",
                "color": "white" if turn == chess.WHITE else "black",
                "is_user": turn == user_color,
                "actual": actual_san,
                "uci": move.uci(),
                "best": best_san,
                "best_uci": best_uci,
                "cp_loss": cp_loss,
                "classification": classify(cp_loss),
                "s1": s1,
                "s2": s2,
                "fen": board.fen(),
            })
            s1, best = s2, next_best
    finally:
        engine.quit()

    return {
        "white": white_name,
        "black": black_name,
        "user_color": "white" if user_color == chess.WHITE else "black",
        "result": game.headers.get("Result", "?"),
        "start_fen": start_fen,
        "moves": evals,
    }


def analyze(pgn_str: str, username: str, sf_path: str, time_per_move: float) -> None:
    game = chess.pgn.read_game(io.StringIO(pgn_str))
    if not game:
        print("Could not parse PGN.")
        return

    white_name = game.headers.get("White", "?")
    black_name = game.headers.get("Black", "?")
    user_side = "White" if white_name.lower() == username.lower() else "Black"

    print(f"\n{'═' * 54}")
    print(f"  GAME ANALYSIS")
    print(f"{'═' * 54}")
    print(f"  {white_name} (W) vs {black_name} (B)")
    print(f"  You played: {user_side}   |   Result: {game.headers.get('Result', '?')}")
    print(f"  Eval: positive = White is better\n")
    print(f"  Analyzing... ({time_per_move}s per move)\n")

    result = analyze_game(pgn_str, username, sf_path, time_per_move)
    user_moves = [m for m in result["moves"] if m["is_user"]]
    blunders = [m for m in user_moves if m["classification"] == "blunder"]
    mistakes = [m for m in user_moves if m["classification"] == "mistake"]
    inaccuracies = [m for m in user_moves if m["classification"] == "inaccuracy"]
    good_moves = sum(1 for m in user_moves if m["classification"] is None)

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
