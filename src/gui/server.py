"""
Local web GUI for visualizing the stats, game, and opening analyzers.

Usage:
    python3 -m src.gui.server
    python3 -m src.gui.server --port 8000
"""

import argparse
import shutil
import webbrowser
from datetime import datetime, timezone
from pathlib import Path

import chess
import chess.svg
from flask import Flask, jsonify, request, send_from_directory, Response

from src import stats, opening_analysis
from src.analyzer import analyze_game, DEFAULT_TIME, BLUNDER_CP, MISTAKE_CP, INACCURACY_CP

STATIC_DIR = Path(__file__).parent / "static"

app = Flask(__name__, static_folder=None)

_games_cache: dict = {"key": None, "games": []}
_analysis_cache: dict[tuple[str, float], dict] = {}


def all_games() -> list[dict]:
    """All local games, reloaded only when the data files change (e.g. after an import)."""
    key = tuple((p.name, p.stat().st_mtime) for p in sorted(stats.DATA_DIR.glob("*.json")))
    if key != _games_cache["key"]:
        _games_cache["games"] = stats.load_all_games()
        _games_cache["key"] = key
    return _games_cache["games"]


def filtered_games() -> list[dict]:
    since = request.args.get("since") or None
    time_class = request.args.get("time_class") or None
    games = all_games()
    if since:
        games = [g for g in games if stats.game_end_month(g) >= since]
    if time_class:
        games = [g for g in games if g.get("time_class") == time_class]
    return games


def game_summary(g: dict) -> dict:
    side = stats.my_side(g)
    opp = "black" if side == "white" else "white"
    ts = g.get("end_time")
    return {
        "url": g.get("url"),
        "date": datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d") if ts else "",
        "end_time": ts or 0,
        "time_class": g.get("time_class"),
        "color": side,
        "result": stats.classify_result(g),
        "my_rating": g[side].get("rating"),
        "opponent": g[opp]["username"],
        "opp_rating": g[opp].get("rating"),
        "opening": stats.opening_name(g),
        "termination": stats.termination(g),
    }


@app.get("/")
def index():
    return send_from_directory(STATIC_DIR, "index.html")


@app.get("/static/<path:name>")
def static_files(name):
    return send_from_directory(STATIC_DIR, name)


@app.get("/api/stats")
def api_stats():
    games = filtered_games()
    return jsonify({"username": stats.USERNAME, **stats.compute_stats(games)})


@app.get("/api/games")
def api_games():
    games = filtered_games()
    q = request.args.get("q", "").lower()
    result = request.args.get("result")
    rows = [game_summary(g) for g in games]
    if q:
        rows = [r for r in rows if q in r["opponent"].lower() or q in r["opening"].lower()]
    if result:
        rows = [r for r in rows if r["result"] == result]
    rows.sort(key=lambda r: r["end_time"], reverse=True)
    limit = request.args.get("limit", 200, type=int)
    return jsonify({"total": len(rows), "games": rows[:limit]})


@app.get("/api/analyze")
def api_analyze():
    url = request.args.get("url", "").rstrip("/")
    time_per_move = request.args.get("time", DEFAULT_TIME, type=float)
    key = (url, time_per_move)
    if key in _analysis_cache:
        return jsonify(_analysis_cache[key])

    sf_path = shutil.which("stockfish")
    if not sf_path:
        return jsonify({"error": "Stockfish not found. Install with: brew install stockfish"}), 500
    game = next((g for g in all_games() if g.get("url", "").rstrip("/") == url), None)
    if not game or not game.get("pgn"):
        return jsonify({"error": f"Game not found in local data: {url}"}), 404

    result = analyze_game(game["pgn"], stats.USERNAME, sf_path, time_per_move)
    if not result:
        return jsonify({"error": "Could not parse PGN."}), 400
    result["summary"] = game_summary(game)
    result["thresholds"] = {"blunder": BLUNDER_CP, "mistake": MISTAKE_CP, "inaccuracy": INACCURACY_CP}
    _analysis_cache[key] = result
    return jsonify(result)


@app.get("/api/openings")
def api_openings():
    """Opening families (by ECO slug) with game counts, for the opening picker."""
    counts: dict[str, int] = {}
    color = request.args.get("color")
    for g in all_games():
        if color and stats.my_side(g) != color:
            continue
        slug = g.get("eco", "").rstrip("/").split("/")[-1]
        if slug:
            name = slug.replace("-", " ")
            counts[name] = counts.get(name, 0) + 1
    ranked = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return jsonify([{"name": n, "games": c} for n, c in ranked])


@app.get("/api/opening_tree")
def api_opening_tree():
    opening = request.args.get("opening", "")
    color = request.args.get("color") or None
    depth = request.args.get("depth", 10, type=int)
    min_games = request.args.get("min_games", 5, type=int)

    pattern = opening.replace(" ", "-").lower()
    matched = [g for g in all_games() if pattern in g.get("eco", "").lower()]
    if color:
        matched = [g for g in matched if stats.my_side(g) == color]
    if not matched:
        return jsonify({"error": f"No games found for '{opening}'"}), 404

    tree = opening_analysis.build_tree(matched, depth)
    white_count = sum(1 for g in matched if stats.my_side(g) == "white")
    return jsonify({
        "opening": opening,
        "color": color,
        "my_color": color or ("white" if white_count > len(matched) / 2 else "black"),
        "tree": opening_analysis.tree_to_dict(tree, 0, depth, min_games, []),
    })


@app.get("/api/board.svg")
def api_board():
    """Renders a position. Pass either fen=... or moves=e4,e5,... (SAN from the start position)."""
    board = chess.Board(request.args.get("fen") or chess.STARTING_FEN)
    lastmove = None
    moves = request.args.get("moves")
    if moves:
        for san in moves.split(","):
            lastmove = board.push_san(san)
    if request.args.get("lastmove"):
        lastmove = chess.Move.from_uci(request.args["lastmove"])

    arrows = []
    if request.args.get("best"):
        best = chess.Move.from_uci(request.args["best"])
        arrows.append(chess.svg.Arrow(best.from_square, best.to_square, color="#1baf7acc"))

    orientation = chess.BLACK if request.args.get("flip") == "1" else chess.WHITE
    svg = chess.svg.board(board, lastmove=lastmove, arrows=arrows, orientation=orientation,
                          size=480, colors={"square light": "#eeeed2", "square dark": "#769656",
                                            "square light lastmove": "#f6f669",
                                            "square dark lastmove": "#baca2b"})
    return Response(svg, mimetype="image/svg+xml")


def main():
    parser = argparse.ArgumentParser(description="Chess analysis GUI")
    parser.add_argument("--port", type=int, default=5050)
    parser.add_argument("--no-browser", action="store_true", help="Don't open a browser tab")
    args = parser.parse_args()

    url = f"http://127.0.0.1:{args.port}"
    print(f"Chess GUI running at {url}  (Ctrl+C to stop)")
    if not args.no_browser:
        webbrowser.open(url)
    app.run(host="127.0.0.1", port=args.port)


if __name__ == "__main__":
    main()
