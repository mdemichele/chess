# Chess Improvement Tool

A personal chess analysis tool that imports your chess.com game history and helps you understand your strengths, weaknesses, and opening patterns.

## What's Been Built

### Game Importer
Downloads your full chess.com game history via the public API and saves it locally as JSON.

```bash
python3 -m src.importer          # import all games
python3 -m src.importer --since 2025-01   # from a specific month
python3 -m src.importer --month 2025-06   # one month only
python3 -m src.importer --force           # re-download everything
```

### Stats Analyzer
Summarizes your record by time control, color, opening, and how games end. Includes a month-by-month rating trend.

```bash
python3 -m src.stats
python3 -m src.stats --time-class rapid
python3 -m src.stats --since 2025-06
```

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

---

## Example Output — mattydem's Stats

```
══════════════════════════════════════════════════
  CHESS STATS — mattydem
══════════════════════════════════════════════════

──────────────────────────────────────────────────
  OVERALL RECORD
──────────────────────────────────────────────────

  1992W / 1979L / 211D  (50.2% score, 4182 games)

──────────────────────────────────────────────────
  BY TIME CONTROL
──────────────────────────────────────────────────

  Blitz     4W / 7L / 1D  (37.5% score, 12 games)
  Rapid     1976W / 1958L / 209D  (50.2% score, 4143 games)
  Daily     12W / 14L / 1D  (46.3% score, 27 games)

──────────────────────────────────────────────────
  BY COLOR
──────────────────────────────────────────────────

  White     1045W / 941L / 104D  (52.5% score, 2090 games)
  Black     947W / 1038L / 107D  (47.8% score, 2092 games)

──────────────────────────────────────────────────
  HOW GAMES END
──────────────────────────────────────────────────

  resignation            2437  (58.3%)
  checkmate              1028  (24.6%)
  abandoned               357  (8.5%)
  stalemate                90  (2.2%)
  repetition               52  (1.2%)

──────────────────────────────────────────────────
  TOP OPENINGS AS WHITE
──────────────────────────────────────────────────

  Opening                                   Games    Win%
  ────────────────────────────────────────  ──────  ──────
  Kings Pawn Opening Kings                    143   54.2%
  Queens Pawn Opening Chigorin                107   54.2%
  Philidor Defense 3.Bc4                       89   60.1%
  Scandinavian Defense Mieses Kotrc            76   49.3%
  Queens Pawn Opening Accelerated              76   57.9%
  Giuoco Piano Game Giuoco                     66   53.0%
  Italian Game                                 59   44.9%
  French Defense Knight Variation              55   62.7%
  Italian Game Two Knights                     51   56.9%
  Scandinavian Defense                         48   47.9%

──────────────────────────────────────────────────
  TOP OPENINGS AS BLACK
──────────────────────────────────────────────────

  Opening                                   Games    Win%
  ────────────────────────────────────────  ──────  ──────
  Kings Pawn Opening 1...e5                   186   55.1%
  Petrovs Defense Three Knights               162   54.0%
  Petrovs Defense Classical Variation          99   52.0%
  Bishops Opening Berlin Defense               95   40.0%
  Petrovs Defense                              84   54.2%
  Kings Pawn Opening Leonardis                 66   45.5%
  Center Game                                  63   44.4%
  Italian Game                                 61   41.0%
  Kings Pawn Opening Kings                     58   40.5%
  Queens Pawn Opening Zukertort                56   41.1%

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
  2026-06              961    1029     893      76
```

---

## Getting Started

**Requirements:** Python 3.10+

```bash
pip install -r requirements.txt
python3 -m src.importer       # download your games
python3 -m src.stats          # view your stats
```

Change `USERNAME = "mattydem"` in `src/importer.py` and `src/stats.py` to use your own chess.com username.

---

## Roadmap

- [ ] Stockfish integration for blunder/mistake detection
- [ ] Tactical pattern recognition
- [ ] Endgame training modules
- [ ] Opening repertoire builder
