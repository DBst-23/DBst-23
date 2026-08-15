# WNBA LIVE-FLOW Postmortem — Washington Mystics at Las Vegas Aces

**Date:** 2026-08-13  
**Venue:** Michelob ULTRA Arena, Las Vegas, NV  
**Checkpoint:** Halftime  
**Halftime score:** Las Vegas 38 — Washington 32  
**Final score:** Las Vegas 83 — Washington 76  
**Final total:** 159  
**Status:** FINAL — two correlated Under losses

## Frozen SharpEdge projection — before sportsbook comparison

The market-blind halftime checkpoint was preserved in `WNBA_LIVEFLOW_CHECKPOINT_WAS_LVA_2026-08-13.md`.

| Market | SharpEdge projection | Actual | Error |
|---|---:|---:|---:|
| Full-game total | 152 | 159 | -7 |
| Las Vegas team total | 82 | 83 | -1 |
| Washington team total | 70 | 76 | -6 |
| Final margin | LVA -12 | LVA -7 | 5 pts |

Projected second half: **Las Vegas 44 — Washington 38**  
Actual second half: **Las Vegas 45 — Washington 44**

The Las Vegas scoring projection was nearly exact. The miss was overwhelmingly Washington-side scoring allocation and efficiency.

## LIVE-FLOW wagers

### Wager 1 — Washington team total
- **Selection:** Washington Mystics team total UNDER 75.5
- **Odds:** -120
- **Stake:** $10.00
- **Sportsbook:** William Hill
- **Ticket timestamp:** AUG 13 2026, 07:58 PM NV
- **Ticket ID:** `1465d670-978c-11f1-9a9f-8df2172ebdb4`
- **Result:** **LOSS**

Washington finished with **76**, losing the wager by **0.5 point**.

### Wager 2 — full-game total
- **Selection:** UNDER 158.5
- **Odds:** -115
- **Stake:** $5.00
- **Sportsbook:** William Hill
- **Ticket timestamp:** AUG 13 2026, 07:59 PM NV
- **Ticket ID:** `3924e190-978c-11f1-b3b1-9b1297e6ac15`
- **Result:** **LOSS**

The game finished at **159**, losing the wager by **0.5 point**.

**Combined exposure:** $15.00  
**Net:** -$15.00

# Primary diagnosis

This was not a broad Las Vegas projection failure. SharpEdge projected Las Vegas at **82** and the Aces scored **83**.

The core miss was Washington:

> **We correctly identified Washington positive-regression signals at halftime, but did not translate them aggressively enough into the scoring projection.**

Washington had 32 at halftime. SharpEdge projected 38 more for a final of 70. Washington actually scored **44** in the second half and finished at 76.

That six-point Washington miss explains almost the entire seven-point full-game total miss.

## What SharpEdge got right

### 1. Las Vegas scoring regression was calibrated well

At halftime Las Vegas was only:

- 38.7% FG
- 26.7% from three
- A'ja Wilson 1/5
- Chelsea Gray 1/5
- Jewell Loyd 0/4

SharpEdge projected **44 second-half points** for Las Vegas. The Aces scored **45**.

That is a strong read.

### 2. The game remained competitive

The checkpoint correctly noted that the six-point halftime margin supported normal competitive rotations. The game stayed close enough for core players to remain active deep into the fourth quarter.

### 3. Washington turnover and free-throw regression were identified

At halftime Washington had:

- 11 turnovers
- only 1/5 FT

The checkpoint explicitly tagged both `WAS_TURNOVER_REGRESSION_UP` and `WAS_FT_REGRESSION_UP`.

Those directions were correct. Washington committed only **6 turnovers in the second half** and went **7/11 at the line**.

The failure was not recognizing the signals. It was **under-converting them into projected points**.

# Where the model broke

## 1. Regression was described qualitatively but under-quantified

The halftime report correctly said Washington's 32-point half was suppressed by turnovers and free-throw shooting rather than by catastrophic field-goal efficiency.

But the final projection still only moved Washington from 32 first-half points to **38 second-half points**.

That was too conservative for a team with multiple live upward-regression channels.

Actual second-half Washington production:

- 44 points
- 17/30 FG — 56.7%
- 3/7 3PT — 42.9%
- 7/11 FT
- 6 turnovers

The lesson is simple: if LIVE-FLOW flags turnover regression, free-throw regression, and stable paint production simultaneously, those cannot remain descriptive notes. They must materially move the simulation mean and upper tail.

## 2. Shakira Austin's individual finishing regression was underweighted

At halftime Austin had:

- 7 points
- 3/9 FG
- 6 rebounds
- 13:33 played

Washington already had **22 paint points** in the first half, and Austin had substantial interior volume despite poor finishing.

She was therefore not merely part of a low-scoring offense. She was a high-volume interior scorer sitting on obvious finishing-regression potential.

Second half Austin:

- **22 points**
- **9/11 FG**
- 4/5 FT

Final:

- **29 points**
- 12/20 FG

This was the single largest player-level source of the team-total failure.

## 3. Stable paint production should have raised Washington's floor

At halftime Washington had **22 points in the paint on 11/20 paint attempts**.

That was already identified as structurally real rather than fluky.

Washington then produced another **28 paint points** in the second half and finished with **50 points in the paint**.

The model treated the paint signal as a reason not to collapse Washington's projection, but it should have done more: it should have raised the Mystics' expected scoring floor and reduced confidence in a team-total Under.

## 4. The Washington team-total Under and full-game Under were the same core thesis twice

This is a critical process lesson.

The full-game Under 158.5 relied heavily on Washington remaining below a normal scoring second half. The Washington TT Under 75.5 relied on the exact same assumption.

Those were not two independent edges.

They were two correlated expressions of one thesis.

When Washington exceeded the model by six points, both wagers failed by 0.5.

This means the process effectively doubled exposure to the same model error.

## 5. The market-gap looked large, but the model's uncertainty was larger than the point estimate implied

SharpEdge fair lines were:

- Total: 152
- Washington TT: 70

William Hill offered:

- Total: 158.5
- Washington TT: 75.5

Nominal gaps:

- **6.5 points** on the full-game total
- **5.5 points** on Washington's team total

Those are meaningful point-estimate gaps, but the halftime state contained explicit upside variance:

- turnover normalization
- free-throw normalization
- stable paint production
- Austin 3/9 on meaningful interior volume
- competitive rotation security

The market-gap gate therefore needs to interact with a regression-risk/tail gate rather than operating alone.

# Model patch — `LIVEFLOW_REGRESSION_TRANSLATION_GATE_v1`

Going forward:

1. **Every flagged regression channel must receive an explicit points adjustment.** Do not leave `TURNOVER_REGRESSION_UP`, `FT_REGRESSION_UP`, or finishing regression as narrative-only notes.
2. For turnover regression, estimate recovered possessions and convert them into expected points using live offensive efficiency rather than a generic qualitative bump.
3. For free-throw regression, estimate expected second-half FTA and conversion from player/team baselines; do not assume first-half misses persist.
4. Add a **player finishing-regression scan** for high-volume rim/interior scorers. A player with strong shot volume but suppressed conversion should widen the team's scoring upper tail.
5. When `PAINT_PRODUCTION_STABLE` and multiple positive-regression tags coexist, reduce confidence in a team-total Under even when the mean remains below market.
6. Require a distribution check: if the sportsbook line is within the model's upper-middle outcome band, downgrade from STRIKE to LEAN/PASS.

# Exposure patch — `LIVEFLOW_CORRELATED_DERIVATIVE_EXPOSURE_GATE_v1`

1. Before placing multiple halftime wagers, identify the **shared causal thesis** behind each position.
2. A team-total Under plus full-game Under driven by that same team's expected scoring suppression must be treated as **one correlated exposure cluster**.
3. Do not count correlated derivatives as separate confirmations of edge.
4. Cap combined stake on one thesis unless each derivative has an independent causal edge.
5. Postmortem correlated losses as one model miss with multiple tickets, not as multiple independent forecasting failures.

## New / reinforced tags

- `REGRESSION_ACKNOWLEDGED_UNDERQUANTIFIED`
- `TURNOVER_REGRESSION_TRANSLATION_MISS`
- `FT_REGRESSION_TRANSLATION_MISS`
- `INTERIOR_FINISHING_REGRESSION_MISS`
- `PAINT_FLOOR_UNDERWEIGHTED`
- `SHARED_THESIS_CORRELATED_EXPOSURE`
- `DERIVATIVE_DUPLICATION_RISK`
- `TEAM_TOTAL_UPPER_TAIL_RISK`

## Final grade

**LAS VEGAS TEAM SCORING READ: A**  
**WASHINGTON TEAM SCORING READ: D+**  
**FULL-GAME TOTAL READ: C-**  
**REGRESSION IDENTIFICATION: A-**  
**REGRESSION QUANTIFICATION: D**  
**EXPOSURE CONSTRUCTION: D**  
**PROCESS VALUE OF POSTMORTEM: HIGH**

## Bottom line

SharpEdge saw the right Washington regression ingredients but did not price them strongly enough.

The Aces projection was essentially correct: **82 projected, 83 actual**. Washington created the miss: **70 projected, 76 actual**.

Most importantly, the two losing tickets were not two separate bad reads. They were the same Washington-scoring suppression thesis expressed twice. The next upgrade is therefore twofold: **quantify positive-regression signals instead of merely naming them, and cap correlated derivative exposure when multiple bets depend on the same team-level assumption.**
