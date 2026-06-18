# The Scholar's Mate — Queen to h5 and the Four-Move Checkmate

The Scholar's Mate is one of the most important traps to know in chess — not because you should try it on strong players, but because beginners will attempt it on you constantly, and falling for it is embarrassing. Once you know the pattern, you'll never lose to it again.

---

## The Setup: 1.e4 e5 2.Qh5

After `1.e4 e5`, White plays `2.Qh5` — bringing the queen out early to h5.

```
     a    b    c    d    e    f    g    h
   ┌────┬────┬────┬────┬────┬────┬────┬────┐
 8 │ r  │ n  │ b  │    │ k  │ b  │ n  │ r  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 7 │ p  │ p  │ p  │ p  │    │ p  │ p  │ p  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 6 │    │    │    │    │    │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 5 │    │    │    │    │ p  │    │    │ Q  │  ← Queen on h5 eyes e5 and f7
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 4 │    │    │    │    │ P  │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 3 │    │    │    │    │    │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 2 │ P  │ P  │ P  │ P  │    │ P  │ P  │ P  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 1 │ R  │ N  │ B  │    │ K  │ B  │ N  │ R  │
   └────┴────┴────┴────┴────┴────┴────┴────┘
   After 2.Qh5 — the queen threatens Qxe5+ and sets up a mate threat on f7
```

The queen has two immediate threats:
1. **3.Qxe5+** — winning the e5 pawn with check (forking the king and rook on h8)
2. Setting up **Qxf7#** — checkmate on f7 if the bishop on c4 joins the attack

This is why it's called the **Danvers Opening** or informally just "the Queen's attack." The Scholar's Mate is the specific checkmate it leads to.

---

## The Checkmate: How it Happens

White needs one more piece — the bishop — to make the f7 threat lethal. The full four-move checkmate:

**1.e4 e5 2.Qh5 Nc6 3.Bc4 Nf6?? 4.Qxf7#**

```
     a    b    c    d    e    f    g    h
   ┌────┬────┬────┬────┬────┬────┬────┬────┐
 8 │ r  │    │ b  │ q  │ k  │ b  │    │ r  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 7 │ p  │ p  │ p  │ p  │    │ Q  │ p  │ p  │  ← Qxf7# — checkmate
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 6 │    │    │ n  │    │    │ n  │    │    │  ← Nf6 was supposed to chase the queen
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 5 │    │    │    │    │ p  │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 4 │    │    │ B  │    │ P  │    │    │    │  ← Bishop protects Qxf7
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 3 │    │    │    │    │    │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 2 │ P  │ P  │ P  │ P  │    │ P  │ P  │ P  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 1 │ R  │ N  │ B  │    │ K  │    │ N  │ R  │
   └────┴────┴────┴────┴────┴────┴────┴────┘
   After 4.Qxf7# — the queen on f7 is protected by Bc4, the king has nowhere to go
```

Black's mistake was `3...Nf6??` — the move looks logical (develop a piece and attack the queen) but it forgets that the queen on f7 would be protected by the bishop on c4. The king is trapped: f8 is covered by the queen, e7 and e8 are covered by White's pieces, and the f7 queen itself delivers check.

---

## Why f7 Is So Dangerous

The f7 square is the weakest point in Black's starting position. It is only defended by the king, and it sits right next to the king's escape squares. A queen landing on f7 with support from Bc4:
- Attacks the king directly (check)
- Covers e8 (king can't go there)
- Is protected by the bishop (king can't take it)
- Leaves the king with no legal moves if other escape squares are covered

This is why so many beginner traps — Scholar's Mate, Fried Liver Attack, Legal's Mate — all revolve around attacking f7.

---

## How Black Defends

Black has several good responses. The key principle: **don't let the queen and bishop team up on f7.**

### Best response: `2...g6`

Chase the queen immediately. The queen has no good square to go to, and Black gets a free developing tempo.

```
     a    b    c    d    e    f    g    h
   ┌────┬────┬────┬────┬────┬────┬────┬────┐
 8 │ r  │ n  │ b  │ q  │ k  │ b  │ n  │ r  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 7 │ p  │ p  │ p  │ p  │    │ p  │    │ p  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 6 │    │    │    │    │    │    │ p  │    │  ← g6 attacks the queen directly
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 5 │    │    │    │    │ p  │    │    │ Q  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 4 │    │    │    │    │ P  │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 3 │    │    │    │    │    │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 2 │ P  │ P  │ P  │ P  │    │ P  │ P  │ P  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 1 │ R  │ N  │ B  │ Q  │ K  │ B  │ N  │ R  │
   └────┴────┴────┴────┴────┴────┴────┴────┘
   After 2...g6 — the queen must retreat, Black is already slightly better
```

After `3.Qf3` or `3.Qe2`, Black plays `3...Nf6` developing normally, and White has wasted a move bringing the queen out too early. Black is fine.

### Also good: `2...Nc6` then `3...g6`

Develop first, then chase the queen on the next move. After `2...Nc6 3.Bc4 g6`, White cannot play `4.Qxe5` because `4...Nxe5` wins the bishop.

### What NOT to do: `2...Nf6??`

Playing `2...Nf6` immediately looks natural — the knight develops and attacks the queen. But it blunders immediately: **3.Qxe5+** forks the king and h8 rook. Black loses material.

```
     a    b    c    d    e    f    g    h
   ┌────┬────┬────┬────┬────┬────┬────┬────┐
 8 │ r  │ n  │ b  │ q  │ k  │ b  │    │ r  │  ← h8 rook is forked
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 7 │ p  │ p  │ p  │ p  │    │ p  │ p  │ p  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 6 │    │    │    │    │    │ n  │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 5 │    │    │    │    │ Q  │    │    │    │  ← Qxe5+ forks king and rook
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 4 │    │    │    │    │ P  │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 3 │    │    │    │    │    │    │    │    │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 2 │ P  │ P  │ P  │ P  │    │ P  │ P  │ P  │
   ├────┼────┼────┼────┼────┼────┼────┼────┤
 1 │ R  │ N  │ B  │ Q  │ K  │ B  │ N  │ R  │
   └────┴────┴────┴────┴────┴────┴────┴────┘
   After 2...Nf6?? 3.Qxe5+ — Black must move the king, then loses the rook
```

---

## Why You Shouldn't Play It (As White)

Against anyone who knows how to defend, `2.Qh5` is a bad move. Here's why:

- **Queens don't belong out early.** The queen is your most valuable piece. Bringing it out before your minor pieces (knights and bishops) means it gets chased around by Black's pawns and knights, losing tempo.
- **You fall behind in development.** Every time Black plays `...g6`, `...Nf6`, or `...Nc6`, they are developing a piece for free while White's queen scrambles to safety.
- **No long-term plan.** If the Scholar's Mate doesn't work, White has no positional foundation — no control of the center, no piece development, just a misplaced queen.

The opening White should play instead is the **Italian Game** (`2.Nf3 Nc6 3.Bc4`) — same bishop attacking f7, but with proper piece development behind it. The threat on f7 is just as real and the position is sound.

---

## Quick Reference

| Move | Verdict | Why |
|---|---|---|
| `2...g6` | Best | Chases the queen immediately, Black gains a tempo |
| `2...Nc6` then `3...g6` | Also good | Develop first, then chase — works fine |
| `2...Nf6??` | Blunder | Loses a rook to `3.Qxe5+` |
| `3...Nf6??` (after Bc4) | Blunder | Loses to `4.Qxf7#` — the Scholar's Mate |
| `2...Qe7` | Playable but passive | Defends e5 and f7, but blocks Black's own development |

**The one rule:** whenever you see `Qh5` followed by `Bc4`, check if f7 is safe. If it's not — play `...g6` immediately.
