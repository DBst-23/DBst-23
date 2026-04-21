# NBA LiveFlow Postmortem — TOR @ CLE — 2026-04-18

## Summary
- **Game:** Toronto Raptors @ Cleveland Cavaliers
- **Final:** Cavaliers 126, Raptors 113
- **Halftime Score:** Raptors 54, Cavaliers 61
- **LiveFlow Focus:** halftime spread / total / team-total validation
- **Postmortem Classification:** continuation environment, not cosmetic inflation

## Final Score Context
Toronto scored **113** and Cleveland scored **126**, producing a **239-point** final. Cleveland won by **13**.

This is an important LiveFlow teaching game because the halftime market looked expensive on first glance, but the second half confirmed the inflation was largely **real**, not fake.

## Halftime Market Context
At halftime, the board had already been pushed upward:
- **Live spread:** Cleveland around -8.5 to -9.5
- **Live total:** 228.5
- **Cleveland team total:** 120.5
- **Toronto team total:** 111.5

That created a dangerous decision zone. A bettor using a lazy rule like "inflated halftime total = auto under" would have been trapped here.

## Why the Inflation Was Real
### 1. Cleveland offensive control was stable
The Cavaliers finished with:
- **126 points**
- **44-81 FG (54.3%)**
- **16-32 from three (50.0%)**
- **24 assists**

This was not one player dragging a weak environment. This was a multi-source offense with sustainable ball movement and spacing.

### 2. Toronto kept enough pressure on the game
The Raptors still finished with:
- **113 points**
- **37-71 FG (52.1%)**
- **13-27 from three (48.1%)**
- **29 assists**

Even while losing, Toronto scored efficiently enough to keep the game from collapsing into a slow under environment.

### 3. Cleveland’s scoring depth validated continuation
Key Cleveland drivers:
- **Donovan Mitchell: 32 PTS**
- **James Harden: 22 PTS, 10 AST**
- **Max Strus: 24 PTS off bench**
- **Evan Mobley: 17 PTS, 7 REB, 4 AST**
- **Jarrett Allen: 10 PTS, 7 REB**

That type of layered offensive production is exactly what separates **real continuation** from **fake inflation**.

### 4. Toronto never fully died offensively
Key Toronto drivers:
- **RJ Barrett: 24 PTS**
- **Scottie Barnes: 21 PTS, 7 AST**
- **Brandon Ingram: 17 PTS, 4 AST**
- **Jamal Shead: 17 PTS**
- **C. Murray-Boyles: 14 PTS off bench**

Because the trailing side stayed alive, the full-game total and both team totals remained viable even with an already-elevated halftime board.

## LiveFlow Board Validation
### What ultimately cashed from the halftime board
- **Cleveland live spread** range around **-8.5 / -9.5** → ✅ covered (won by 13)
- **Live total 228.5** → ✅ over (final 239)
- **Cleveland team total 120.5** → ✅ over (finished 126)
- **Toronto team total 111.5** → ✅ over (finished 113)

## Diagnostic Lesson
This was **not** a regression game.

It was a **true continuation environment** where:
- the leading side had real offensive stability
- the trailing side had enough shotmaking to preserve pace and pressure
- the halftime market looked expensive, but the underlying environment justified the repricing

## Diagnostic Tags
- `LIVEFLOW_POSTMORTEM`
- `CONTINUATION_ENVIRONMENT_CONFIRMED`
- `HALFTIME_INFLATION_REAL`
- `SPREAD_CONTINUATION_VALIDATED`
- `TEAM_TOTAL_CONTINUATION_VALIDATED`
- `TOTAL_CONTINUATION_VALIDATED`
- `NO_AUTO_UNDER_RULE`

## Model Relevance Summary
This game should be retained as a core LiveFlow training example.

### What the model should learn
Do **not** treat every inflated halftime number as fake.

Instead, separate:
- **Cosmetic inflation** → driven by fragile variance, unstable shotmaking, or unsustainable whistles
- **Real inflation** → driven by scalable offense, multiple scorers, active ball movement, and a trailing opponent that can still score enough to keep the game environment alive

TOR @ CLE belongs in the second category.

This file should be referenced when sharpening:
- halftime total fade logic
- continuation vs regression classification
- spread carry-through validation
- team-total persistence filters

---

## Addendum — LiveFlow Bet Result: Toronto Team Total Under 114.5

### Bet Details
- **Bet:** Toronto Raptors Team Total Under 114.5
- **Entry Timing:** LiveFlow, halftime range
- **Result:** ✅ WIN
- **Final Toronto Score:** 105
- **Margin vs Line:** 9.5 points under

### Why the Bet Won
This under cashed despite Toronto finishing with:
- **42 rebounds**
- **12 offensive rebounds**
- **19 second-chance points**
- **50.6% FG**

That matters because it confirms the original LiveFlow read was based on **true scoring ceiling**, not just possession count.

Toronto generated extra possessions, but their half-court offense still lacked enough reliable top-end creation to threaten **115+**.

### Key Drivers
1. **Brandon Ingram scoring collapse**
   - Finished with **7 points**
   - Shot **3-15 FG**
   - Added **5 turnovers**
   - This removed a major scoring engine from Toronto’s team-total path

2. **Second-chance pressure did not fully convert into ceiling scoring**
   - Toronto posted **12 offensive rebounds**
   - Toronto posted **19 second-chance points**
   - Even with those boosts, they still finished only at **105**

3. **Cleveland controlled game flow**
   - Cleveland scored **115**
   - Offensive efficiency stayed strong enough to keep Toronto chasing
   - Toronto never built the stable multi-source creation needed to break through the number

4. **The halftime requirement was simply too steep**
   - At entry, Toronto needed a major second-half surge
   - They fell short of that path and never seriously threatened the line late

### Diagnostic Tags
- `LIVEFLOW_WIN`
- `TEAM_TOTAL_UNDER_CONFIRMED`
- `PRIMARY_SCORER_FAILURE`
- `SECOND_CHANCE_NOISE_OVERRIDDEN`
- `HALFCOURT_CEILING_LIMIT`
- `EDGE_CALL_ACTIVE`

### Model Relevance
This addendum should reinforce a specific LiveFlow principle:

**Offensive rebounds and second-chance points alone do not invalidate a team-total under if the primary creators are unstable and the half-court ceiling remains capped.**

Toronto had enough possession support to look dangerous, but not enough real creation quality to get near **115**.
