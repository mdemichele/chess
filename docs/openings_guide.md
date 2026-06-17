# Common Chess Openings Guide

A visual guide to the openings you actually encounter — based on your chess.com game history.

---

## How Openings Work

An opening is the first phase of a chess game, typically the first 10–15 moves. Both players are trying to:
- **Control the center** (the d4, d5, e4, e5 squares)
- **Develop pieces** (get knights and bishops off the back rank)
- **Castle** (tuck the king away safely)

Openings are named and categorized by the first few moves played. The same position can be reached by different move orders, but the names help players communicate and study patterns.

---

## The Opening Tree

Most of your games start with 1.e4 (White pushes the king's pawn). Here's how the major openings branch from there:

```
1.e4
├── 1...e5  (Black mirrors — "Open Games")
│   ├── 2.Nf3
│   │   ├── 2...Nc6  →  Italian Game / Ruy Lopez / Scotch Game
│   │   ├── 2...Nf6  →  Petrov's Defense
│   │   └── 2...d6   →  Philidor Defense
│   ├── 2.Bc4        →  Bishop's Opening
│   └── 2.d4         →  Center Game
│
├── 1...d5           →  Scandinavian Defense
├── 1...e6           →  French Defense
└── 1...c6           →  Caro-Kann Defense

1.d4
├── 1...d5  2.c4     →  Queen's Gambit
└── 1...d5  2.Nf3 3.Bf4  →  London System
```

---

## Part 1 — Open Games (1.e4 e5)

When both players push their king's pawn two squares, the game is "open." Pieces have lots of room to move and games tend to be tactical and sharp.

```
     a    b    c    d    e    f    g    h
   ┌────┬────┬────┬────┬────┬────┬────┬────┐
 8 │ r  │ n  │ b  │ q  │ k  │ b  │ n  │ r  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 7 │ p  │ p  │ p  │ p  │    │ p  │ p  │ p  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 6 │    │    │    │    │    │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 5 │    │    │    │    │ p  │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 4 │    │    │    │    │ P  │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 3 │    │    │    │    │    │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 2 │ P  │ P  │ P  │ P  │    │ P  │ P  │ P  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 1 │ R  │ N  │ B  │ Q  │ K  │ B  │ N  │ R  │
   └────┴────┴────┴────┴────┴────┴────┴────┘
   After 1.e4 e5 — both center pawns advance, the game is open
```

---

### Italian Game

**Moves:** `1.e4 e5 2.Nf3 Nc6 3.Bc4`

White develops the knight to f3 (attacking e5), then the bishop to c4 (pointing at the weak f7 pawn near Black's king). One of the oldest and most popular openings.

```
     a    b    c    d    e    f    g    h
   ┌────┬────┬────┬────┬────┬────┬────┬────┐
 8 │ r  │    │ b  │ q  │ k  │ b  │ n  │ r  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 7 │ p  │ p  │ p  │ p  │    │ p  │ p  │ p  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 6 │    │    │ n  │    │    │    │    │    │  ← Black knight defends e5
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 5 │    │    │    │    │ p  │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 4 │    │    │ B  │    │ P  │    │    │    │  ← White bishop eyes f7
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 3 │    │    │    │    │    │ N  │    │    │  ← White knight attacks e5
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 2 │ P  │ P  │ P  │ P  │    │ P  │ P  │ P  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 1 │ R  │ N  │ B  │ Q  │ K  │    │    │ R  │
   └────┴────┴────┴────┴────┴────┴────┴────┘
   After 3.Bc4 — White has developed two pieces and threatens f7
```

**Common continuations:**
- `3...Bc5` — the **Giuoco Piano** ("quiet game"). Black mirrors with their own bishop. Solid and symmetrical.
- `3...Nf6` — the **Two Knights Defense**. Black counterattacks immediately instead of mirroring.

**In your games:** Appears as both White and Black — below average results on both sides (~45%). The Two Knights line (3...Nf6) is your best response as Black at 56%.

---

### Ruy Lopez (Spanish Opening)

**Moves:** `1.e4 e5 2.Nf3 Nc6 3.Bb5`

Instead of aiming the bishop at f7, White pins Black's knight on c6 — the knight that defends the e5 pawn. White is indirectly threatening to win the e5 pawn by removing its defender.

```
     a    b    c    d    e    f    g    h
   ┌────┬────┬────┬────┬────┬────┬────┬────┐
 8 │ r  │    │ b  │ q  │ k  │ b  │ n  │ r  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 7 │ p  │ p  │ p  │ p  │    │ p  │ p  │ p  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 6 │    │    │ n  │    │    │    │    │    │  ← This knight is pinned by Bb5
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 5 │    │ B  │    │    │ p  │    │    │    │  ← White bishop pins the knight
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 4 │    │    │    │    │ P  │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 3 │    │    │    │    │    │ N  │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 2 │ P  │ P  │ P  │ P  │    │ P  │ P  │ P  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 1 │ R  │ N  │ B  │ Q  │ K  │    │    │ R  │
   └────┴────┴────┴────┴────┴────┴────┴────┘
   After 3.Bb5 — the bishop on b5 "pins" the c6 knight against the king
```

The Ruy Lopez is one of the most deeply studied openings in chess history. White gets long-term pressure; Black has many ways to fight back.

**In your games:** You see this ~36 times. It's a standard opponent weapon at your level.

---

### Scotch Game

**Moves:** `1.e4 e5 2.Nf3 Nc6 3.d4`

White immediately strikes at the center with the d-pawn, forcing Black to deal with it right away. More direct and tactical than the Italian or Ruy Lopez.

```
     a    b    c    d    e    f    g    h
   ┌────┬────┬────┬────┬────┬────┬────┬────┐
 8 │ r  │    │ b  │ q  │ k  │ b  │ n  │ r  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 7 │ p  │ p  │ p  │ p  │    │ p  │ p  │ p  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 6 │    │    │ n  │    │    │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 5 │    │    │    │    │ p  │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 4 │    │    │    │ P  │ P  │    │    │    │  ← d4 directly challenges e5
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 3 │    │    │    │    │    │ N  │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 2 │ P  │ P  │ P  │    │    │ P  │ P  │ P  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 1 │ R  │ N  │ B  │ Q  │ K  │ B  │    │ R  │
   └────┴────┴────┴────┴────┴────┴────┴────┘
   After 3.d4 — White attacks the center immediately
```

After `3...exd4 4.Nxd4`, White has a strong knight in the center. Black has several responses — the most common is `4...Nf6` or `4...Bc5`.

---

### Petrov's Defense (Russian Game)

**Moves:** `1.e4 e5 2.Nf3 Nf6`

Instead of defending e5 with a knight (`2...Nc6`), Black immediately counterattacks White's e4 pawn with their own knight. Black is saying: "you attack my pawn, I attack yours."

```
     a    b    c    d    e    f    g    h
   ┌────┬────┬────┬────┬────┬────┬────┬────┐
 8 │ r  │ n  │ b  │ q  │ k  │ b  │    │ r  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 7 │ p  │ p  │ p  │ p  │    │ p  │ p  │ p  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 6 │    │    │    │    │    │ n  │    │    │  ← Black knight attacks e4
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 5 │    │    │    │    │ p  │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 4 │    │    │    │    │ P  │    │    │    │  ← White pawn now under attack
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 3 │    │    │    │    │    │ N  │    │    │  ← White knight attacked e5
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 2 │ P  │ P  │ P  │ P  │    │ P  │ P  │ P  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 1 │ R  │ N  │ B  │ Q  │ K  │ B  │    │ R  │
   └────┴────┴────┴────┴────┴────┴────┴────┘
   After 2...Nf6 — Black counterattacks instead of defending
```

The Petrov tends to lead to solid, symmetrical positions that are hard for White to break through. It has a reputation as a "drawing weapon" at the top level but is perfectly aggressive at club level.

**In your games:** This is your most-played black opening by a wide margin (~323 games). Your win rate is solid at 52–54% across the main lines.

---

### Philidor Defense

**Moves:** `1.e4 e5 2.Nf3 d6`

Black supports the e5 pawn with the d-pawn instead of developing a knight. It's solid but passive — the c8 bishop gets locked behind the d6 pawn.

```
     a    b    c    d    e    f    g    h
   ┌────┬────┬────┬────┬────┬────┬────┬────┐
 8 │ r  │ n  │ b  │ q  │ k  │ b  │ n  │ r  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 7 │ p  │ p  │ p  │    │    │ p  │ p  │ p  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 6 │    │    │    │ p  │    │    │    │    │  ← d6 supports e5 but blocks c8 bishop
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 5 │    │    │    │    │ p  │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 4 │    │    │    │    │ P  │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 3 │    │    │    │    │    │ N  │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 2 │ P  │ P  │ P  │ P  │    │ P  │ P  │ P  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 1 │ R  │ N  │ B  │ Q  │ K  │ B  │    │ R  │
   └────┴────┴────┴────┴────┴────┴────┴────┘
   After 2...d6 — solid but the c8 bishop has no future for now
```

**In your games:** You face this as White about 99 times and score 60% — one of your best results as White.

---

### Bishop's Opening

**Moves:** `1.e4 e5 2.Bc4`

White develops the bishop to c4 immediately, before the knight. Like the Italian Game, the bishop targets f7. White skips Nf3 so the f-pawn is free to advance (f4) later.

```
     a    b    c    d    e    f    g    h
   ┌────┬────┬────┬────┬────┬────┬────┬────┐
 8 │ r  │ n  │ b  │ q  │ k  │ b  │ n  │ r  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 7 │ p  │ p  │ p  │ p  │    │ p  │ p  │ p  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 6 │    │    │    │    │    │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 5 │    │    │    │    │ p  │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 4 │    │    │ B  │    │ P  │    │    │    │  ← Bishop skips straight to c4
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 3 │    │    │    │    │    │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 2 │ P  │ P  │ P  │ P  │    │ P  │ P  │ P  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 1 │ R  │ N  │ B  │ Q  │ K  │    │ N  │ R  │
   └────┴────┴────┴────┴────┴────┴────┴────┘
   After 2.Bc4 — the bishop goes to c4 before the knight develops
```

**Berlin Defense** (`2...Nf6`) is Black's most common response — the knight attacks e4 immediately. This is the line you struggle with as Black (40% win rate). After White plays 3.d3, you do fine (52%); after 3.Nf3, you collapse to 34%.

---

### Center Game

**Moves:** `1.e4 e5 2.d4`

White immediately strikes at the center. After Black captures (`2...exd4`), White recaptures with the queen (`3.Qxd4`), which brings the queen out early — generally considered a slight inaccuracy since the queen can be chased around.

```
     a    b    c    d    e    f    g    h
   ┌────┬────┬────┬────┬────┬────┬────┬────┐
 8 │ r  │ n  │ b  │ q  │ k  │ b  │ n  │ r  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 7 │ p  │ p  │ p  │ p  │    │ p  │ p  │ p  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 6 │    │    │    │    │    │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 5 │    │    │    │    │ p  │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 4 │    │    │    │ P  │ P  │    │    │    │  ← d4 immediately challenges e5
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 3 │    │    │    │    │    │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 2 │ P  │ P  │ P  │    │    │ P  │ P  │ P  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 1 │ R  │ N  │ B  │ Q  │ K  │ B  │ N  │ R  │
   └────┴────┴────┴────┴────┴────┴────┴────┘
   After 2.d4 — White attacks both center squares at once
```

**In your games:** You face this ~67 times. Respond with `2...exd4` to take the pawn, then develop with `3...Nc6` to chase White's queen.

---

## Part 2 — Semi-Open Games (1.e4, Black plays something else)

Black declines to mirror with 1...e5, instead choosing an asymmetrical setup. These games tend to be less tactical early on but lead to rich middlegames.

---

### Scandinavian Defense

**Moves:** `1.e4 d5`

Black immediately attacks White's e4 pawn with the d-pawn. After `2.exd5`, Black usually recaptures with the queen (`2...Qxd5`), which comes out early but is not as dangerous as it looks.

```
     a    b    c    d    e    f    g    h
   ┌────┬────┬────┬────┬────┬────┬────┬────┐
 8 │ r  │ n  │ b  │ q  │ k  │ b  │ n  │ r  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 7 │ p  │ p  │ p  │    │ p  │ p  │ p  │ p  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 6 │    │    │    │    │    │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 5 │    │    │    │ p  │    │    │    │    │  ← d5 immediately challenges e4
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 4 │    │    │    │    │ P  │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 3 │    │    │    │    │    │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 2 │ P  │ P  │ P  │ P  │    │ P  │ P  │ P  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 1 │ R  │ N  │ B  │ Q  │ K  │ B  │ N  │ R  │
   └────┴────┴────┴────┴────┴────┴────┴────┘
   After 1...d5 — Black immediately fights for the center
```

**In your games:** You face this ~51 times as White and score 49%. A common Black strategy is to retreat the queen to d6 or a5 after White chases it with Nc3.

---

### French Defense

**Moves:** `1.e4 e6`

Black prepares to challenge the center with `2...d5` on the next move, but first shields the bishop check on b5. The trade-off: the c8 bishop gets locked behind the e6 pawn and can be a problem all game.

```
     a    b    c    d    e    f    g    h
   ┌────┬────┬────┬────┬────┬────┬────┬────┐
 8 │ r  │ n  │ b  │ q  │ k  │ b  │ n  │ r  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 7 │ p  │ p  │ p  │ p  │    │ p  │ p  │ p  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 6 │    │    │    │    │ p  │    │    │    │  ← e6 prepares d5 next move
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 5 │    │    │    │    │    │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 4 │    │    │    │    │ P  │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 3 │    │    │    │    │    │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 2 │ P  │ P  │ P  │ P  │    │ P  │ P  │ P  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 1 │ R  │ N  │ B  │ Q  │ K  │ B  │ N  │ R  │
   └────┴────┴────┴────┴────┴────┴────┴────┘
   After 1...e6 — solid but the c8 bishop will be a long-term problem
```

**In your games:** You face this as White ~34 times and score a strong 62% — your best result against any black opening. The Knight Variation (2.Nf3) is your go-to, and it's working.

---

### Caro-Kann Defense

**Moves:** `1.e4 c6`

Similar idea to the French — Black prepares `2...d5` to challenge the center — but the c6 pawn doesn't block the c8 bishop the way e6 does in the French. Black gets a solid pawn structure; White gets more space.

```
     a    b    c    d    e    f    g    h
   ┌────┬────┬────┬────┬────┬────┬────┬────┐
 8 │ r  │ n  │ b  │ q  │ k  │ b  │ n  │ r  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 7 │ p  │ p  │    │ p  │ p  │ p  │ p  │ p  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 6 │    │    │ p  │    │    │    │    │    │  ← c6 supports d5 next move
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 5 │    │    │    │    │    │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 4 │    │    │    │    │ P  │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 3 │    │    │    │    │    │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 2 │ P  │ P  │ P  │ P  │    │ P  │ P  │ P  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 1 │ R  │ N  │ B  │ Q  │ K  │ B  │ N  │ R  │
   └────┴────┴────┴────┴────┴────┴────┴────┘
   After 1...c6 — like the French but the c8 bishop stays free
```

**In your games:** You face this ~25 times. A standard plan for White is 2.d4 d5 3.Nc3 (or 3.Nd2), fighting for the center.

---

## Part 3 — Queen's Pawn Games (1.d4)

When White opens with the d-pawn instead of the e-pawn, the game tends to be more strategic and slower to open up.

---

### Queen's Gambit

**Moves:** `1.d4 d5 2.c4`

White offers the c4 pawn as a "gambit" — Black can take it (`2...dxc4`, **Queen's Gambit Accepted**) or decline (`2...e6`, **Queen's Gambit Declined**). White's goal is to control the center with the d4 pawn while gaining space on the queenside.

```
     a    b    c    d    e    f    g    h
   ┌────┬────┬────┬────┬────┬────┬────┬────┐
 8 │ r  │ n  │ b  │ q  │ k  │ b  │ n  │ r  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 7 │ p  │ p  │ p  │    │ p  │ p  │ p  │ p  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 6 │    │    │    │    │    │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 5 │    │    │    │ p  │    │    │    │    │  ← Black defends center with d5
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 4 │    │    │ P  │ P  │    │    │    │    │  ← c4 offered as gambit
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 3 │    │    │    │    │    │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 2 │ P  │ P  │    │    │ P  │ P  │ P  │ P  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 1 │ R  │ N  │ B  │ Q  │ K  │ B  │ N  │ R  │
   └────┴────┴────┴────┴────┴────┴────┴────┘
   After 2.c4 — the gambit pawn is offered; Black can take or decline
```

Despite the name, the Queen's Gambit is not a true gambit — if Black takes the pawn, White almost always wins it back. It's about fighting for the center, not sacrificing material.

---

### London System

**Moves:** `1.d4 d5 2.Nf3 Nf6 3.Bf4`

A solid, easy-to-learn White system. White sets up the same structure every game: pawns on d4 and e3, knight on f3, bishop on f4. It's very hard for Black to find a knockout blow against it, and White has a clear plan.

```
     a    b    c    d    e    f    g    h
   ┌────┬────┬────┬────┬────┬────┬────┬────┐
 8 │ r  │ n  │ b  │ q  │ k  │ b  │    │ r  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 7 │ p  │ p  │ p  │    │ p  │ p  │ p  │ p  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 6 │    │    │    │    │    │ n  │    │    │  ← Black mirrors with Nf6
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 5 │    │    │    │ p  │    │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 4 │    │    │    │ P  │    │ B  │    │    │  ← Bf4 is the London's signature move
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 3 │    │    │    │    │    │ N  │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 2 │ P  │ P  │ P  │    │ P  │ P  │ P  │ P  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 1 │ R  │ N  │    │ Q  │ K  │ B  │    │ R  │
   └────┴────┴────┴────┴────┴────┴────┴────┘
   After 3.Bf4 — the London's signature bishop move
```

**In your games:** You play the Accelerated London System ~74 times and score 58% — one of your strongest white openings.

---

## Quick Reference

| Opening | Moves | You Play It? | Your Score |
|---|---|---|---|
| Italian Game | 1.e4 e5 2.Nf3 Nc6 3.Bc4 | Both colors | ~45% |
| Ruy Lopez | 1.e4 e5 2.Nf3 Nc6 3.Bb5 | vs. you | — |
| Scotch Game | 1.e4 e5 2.Nf3 Nc6 3.d4 | vs. you | — |
| Petrov's Defense | 1.e4 e5 2.Nf3 Nf6 | As Black | **53%** |
| Philidor Defense | 1.e4 e5 2.Nf3 d6 | As White | **60%** |
| Bishop's Opening | 1.e4 e5 2.Bc4 | vs. you | 40% as Black |
| Center Game | 1.e4 e5 2.d4 | vs. you | — |
| Scandinavian Defense | 1.e4 d5 | As White | 49% |
| French Defense | 1.e4 e6 | As White | **62%** |
| Caro-Kann Defense | 1.e4 c6 | As White | — |
| Queen's Gambit | 1.d4 d5 2.c4 | — | — |
| London System | 1.d4 d5 2.Nf3 3.Bf4 | As White | **58%** |
