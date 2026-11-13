# Chess Improvement Tool

A personal chess analysis tool that imports your chess.com game history and helps you understand your strengths, weaknesses, and opening patterns. Everything can be run from the command line or explored visually in a local web GUI.

## What's Been Built

### GUI
A local web app for visualizing everything below. Start it with:

```bash
python3 -m src.gui.server              # opens http://127.0.0.1:5050
python3 -m src.gui.server --port 8000 --no-browser
```

- **Overview** — rating trend chart, results by time control and color, how games end, and your top openings as White and Black. Filter by time control and start month.
- **Games** — search and filter your games, then click one to analyze it with Stockfish: an interactive board, an evaluation graph with your errors marked, and a list of your blunders, mistakes, and inaccuracies with the engine's best move drawn as an arrow. Use ←/→ (and Home/End) to step through moves.
- **Openings** — an interactive move tree for any opening with per-branch win/draw/loss results. Branches where you score below 45% are flagged. Clicking an opening on the Overview opens its tree.
- **↻ Refresh data** — downloads your newest games from chess.com (same as `importer --latest`) and updates every view.

### Game Importer
Downloads your full chess.com game history via the public API and saves it locally as JSON.

```bash
python3 -m src.importer          # import all games
python3 -m src.importer --since 2025-01   # from a specific month
python3 -m src.importer --month 2025-06   # one month only
python3 -m src.importer --force           # re-download everything
python3 -m src.importer --latest          # update to your newest games
```

To keep your data current, use `--latest`: it re-downloads your most recent saved month (which may have been saved mid-month) and fetches every month after it. A plain import skips months that are already saved.

### Stats Analyzer
Summarizes your record by time control, color, opening, and how games end. Includes a month-by-month rating trend.

```bash
python3 -m src.stats
python3 -m src.stats --time-class rapid
python3 -m src.stats --since 2025-06
```

### Game Analyzer (Stockfish)
Analyzes a specific game move-by-move using Stockfish, identifying blunders, mistakes, and inaccuracies and showing the best alternative for each error.

```bash
python3 -m src.analyzer https://www.chess.com/game/live/12345
python3 -m src.analyzer https://www.chess.com/game/live/12345 --time 0.5   # slower = stronger
```

The game must already be downloaded locally (run the importer first). Requires Stockfish: `brew install stockfish`.

### Opening Analyzer
Builds a move-by-move win rate tree for any opening, showing where your results diverge based on which continuation you choose.

```bash
python3 -m src.opening_analysis "Italian Game"
python3 -m src.opening_analysis "Bishops Opening Berlin Defense" --color black
python3 -m src.opening_analysis "Petrovs Defense" --depth 12
```

### Documentation
- `docs/chess_notation_guide.md` — visual guide to reading chess notation, with ASCII board diagrams
- `docs/openings_guide.md` — overview of 13 common openings drawn from real game history, all positions machine-verified
- `docs/italian_game_guide.md` — in-depth guide to the Italian Game covering the Giuoco Piano, Two Knights Defense, Evans Gambit, and strategic plans for both sides
- `docs/scholars_mate_guide.md` — guide to the Scholar's Mate (2.Qh5), how the four-move checkmate works, and how to defend against it as Black

---

## Example Output — mattydem's Stats

```
══════════════════════════════════════════════════
  CHESS STATS — mattydem
══════════════════════════════════════════════════

──────────────────────────────────────────────────
  OVERALL RECORD
──────────────────────────────────────────────────

  2400W / 2377L / 243D  (50.2% score, 5020 games)

──────────────────────────────────────────────────
  BY TIME CONTROL
──────────────────────────────────────────────────

  Blitz     4W / 7L / 1D  (37.5% score, 12 games)
  Rapid     2380W / 2356L / 241D  (50.2% score, 4977 games)
  Daily     16W / 14L / 1D  (53.2% score, 31 games)

──────────────────────────────────────────────────
  BY COLOR
──────────────────────────────────────────────────

  White     1264W / 1122L / 122D  (52.8% score, 2508 games)
  Black     1136W / 1255L / 121D  (47.6% score, 2512 games)

──────────────────────────────────────────────────
  HOW GAMES END
──────────────────────────────────────────────────

  resignation            2923  (58.2%)
  checkmate              1210  (24.1%)
  abandoned               464  (9.2%)
  stalemate                99  (2.0%)
  repetition               62  (1.2%)

──────────────────────────────────────────────────
  TOP OPENINGS AS WHITE
──────────────────────────────────────────────────

  Opening                                   Games    Win%
  ────────────────────────────────────────  ──────  ──────
  Kings Pawn Opening Kings                    154   56.2%
  Giuoco Piano Game Giuoco                    119   57.1%
  Queens Pawn Opening Chigorin                117   53.0%
  Scandinavian Defense Mieses Kotrc           109   51.4%
  Philidor Defense 3.Bc4                      104   61.1%
  Italian Game Two Knights                     89   51.1%
  Italian Game                                 83   51.8%
  Queens Pawn Opening Accelerated              79   58.2%
  French Defense Knight Variation              64   60.2%
  Scandinavian Defense                         54   49.1%

──────────────────────────────────────────────────
  TOP OPENINGS AS BLACK
──────────────────────────────────────────────────

  Opening                                   Games    Win%
  ────────────────────────────────────────  ──────  ──────
  Petrovs Defense Three Knights               222   53.6%
  Kings Pawn Opening 1...e5                   213   52.1%
  Petrovs Defense Classical Variation         148   49.0%
  Bishops Opening Berlin Defense              127   38.6%
  Petrovs Defense                             110   50.5%
  Kings Pawn Opening Leonardis                 91   50.5%
  Center Game                                  70   45.7%
  Queens Pawn Opening Zukertort                68   38.2%
  Italian Game                                 63   39.7%
  Queens Pawn Opening 1...d5                   62   43.5%

──────────────────────────────────────────────────
  RATING TREND
──────────────────────────────────────────────────

  Month         Avg Rating    Peak     Low   Games
  ──────────  ────────────  ──────  ──────  ──────
  2024-11              510    1273     400     453
  2024-12              523    1004     408     472
  2025-01              648    1038     566     352
  2025-03              813     884     345     198
  2025-06              804     901     752     245
  2025-09              895    1158     827     235
  2025-12              995    1133     920     187
  2026-03             1010    1062     907     123
  2026-06              977    1032     893     164
  2026-09              965    1228     857     185
  2026-11              971    1021     942      62
```

---

## Getting Started

**Requirements:** Python 3.10+, and [Stockfish](https://stockfishchess.org/) for game analysis (`brew install stockfish`)

```bash
python3 -m pip install -r requirements.txt
python3 -m src.importer       # download your games
python3 -m src.stats          # view your stats
python3 -m src.gui.server     # or explore everything in the browser
```

To use your own chess.com username, change `USERNAME = "mattydem"` in `src/importer.py`, `src/stats.py`, `src/analyzer.py`, and `src/opening_analysis.py`.

Run all commands from the repository root. If `pip` gives errors, use `python3 -m pip` so packages install into the same Python that runs the tool.

---

## Roadmap

- [x] Stockfish integration for blunder/mistake detection
- [x] Web GUI for visualizing stats, game analysis, and opening trees
- [x] One-click refresh of the newest chess.com games
- [ ] Tactical pattern recognition
- [ ] Endgame training modules
- [ ] Opening repertoire builder
